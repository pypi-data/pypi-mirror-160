import io
import json
import socket
import shlex
import tarfile
import zipfile
from time import time, sleep
from queue import Queue
import multiprocessing
import os
import signal
from types import FrameType

import requests
from docker.errors import ImageNotFound  # type: ignore
from docker.models.networks import Network  # type: ignore
from docker.models.containers import Container  # type: ignore

from biolib.biolib_binary_format.stdout_and_stderr import StdoutAndStderr
from biolib.compute_node.job_worker.job_storage import JobStorage
from biolib.compute_node.job_worker.large_file_system import LargeFileSystem
from biolib.biolib_errors import DockerContainerNotFoundDuringExecutionException, RetryException
from biolib.compute_node.job_worker.job_max_runtime_timer_thread import JobMaxRuntimeTimerThread
from biolib.compute_node.remote_host_proxy import RemoteHostProxy
from biolib.typing_utils import Optional, List, Dict
from biolib import utils
from biolib.biolib_api_client import ModuleEnvironment, Job, JobWrapper, Module, AppVersionOnJob, BiolibApiClient, \
    RemoteHost
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_docker_client import BiolibDockerClient
from biolib.biolib_singularity_client import BiolibSingularityClient
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.compute_node.job_worker.executors import DockerExecutor, SingularityExecutor
from biolib.compute_node.job_worker.executors.base_executor import BaseExecutor
from biolib.compute_node.job_worker.executors.types import LocalExecutorOptions, StatusUpdate
from biolib.compute_node.socker_listener_thread import SocketListenerThread
from biolib.compute_node.socket_sender_thread import SocketSenderThread
from biolib.compute_node.job_worker.mappings import Mappings, path_without_first_folder
from biolib.compute_node.job_worker.utils import ComputeProcessException, log_disk_and_memory_usage_info
from biolib.compute_node.utils import get_package_type, SystemExceptionCodes, SystemExceptionCodeMap
from biolib.biolib_binary_format import SavedJob, SystemStatusUpdate, ModuleInput, SystemException

_DNS_PROXY_IMAGE_URI = 'spx01/blocky@sha256:485ef739233341d3e14a64db646754aba7322c34645f804c3c0c00556d9a2cd1'
DEFAULT_BUFFER_SIZE = 1024
SOCKET_HOST = '127.0.0.1'


class JobWorkerProcess(multiprocessing.Process):

    # note: this method is run in the parent process
    def __init__(self, socket_port: int, log_level: int):
        super().__init__()
        self._socket_port = socket_port
        self._log_level = log_level

    # note: this method is run in the newly started process once called with .start()
    def run(self) -> None:
        _JobWorker(self._socket_port, self._log_level).run_handle_message_loop()


class _JobWorker:
    _STOP_HANDLE_MESSAGE_LOOP = b'STOP_HANDLE_MESSAGE_LOOP'

    def __init__(self, socket_port: int, log_level: int):
        try:
            logger.setLevel(log_level)

            # handle interrupt from keyboard (CTRL + C)
            signal.signal(signal.SIGINT, self._handle_exit_gracefully)
            # handle termination signal from parent
            signal.signal(signal.SIGTERM, self._handle_exit_gracefully)

            self._socket_port = socket_port
            self._received_messages_queue: Queue = Queue()
            self._messages_to_send_queue: Queue = Queue()

            self._app_version_id_to_runtime_zip: Dict[str, bytes] = {}
            self._jobs: Dict[str, Job] = {}
            self._root_job_wrapper: Optional[JobWrapper] = None

            self._dns_proxy: Optional[Container] = None

            self._remote_host_proxies: List[RemoteHostProxy] = []
            self._internal_network: Optional[Network] = None
            self._public_network: Optional[Network] = None
            self._executors: List[BaseExecutor] = []
            self.is_cleaning_up: bool = False

            self.job_temporary_dir: Optional[str] = None

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_INIT_COMPUTE_PROCESS_VARIABLES.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception

        self._connect_to_parent()

    def _handle_exit_gracefully(self, signum: int, frame: FrameType) -> None:  # pylint: disable=unused-argument
        logger_no_user_data.debug(
            f'_JobWorker got exit signal {signal.Signals(signum).name}'  # pylint: disable=no-member
        )
        self._received_messages_queue.put(self._STOP_HANDLE_MESSAGE_LOOP)
        self._cleanup()

    def run_handle_message_loop(self):
        logger_no_user_data.debug(f'Started JobWorkerProcess {os.getpid()}')
        while True:
            try:
                package = self._received_messages_queue.get()
                if package == self._STOP_HANDLE_MESSAGE_LOOP:
                    break

                package_type = get_package_type(package)
                if package_type == 'SavedJob':
                    self._handle_save_job_wrapper(package)
                    if utils.IS_RUNNING_IN_CLOUD:
                        job = self._root_job_wrapper['job']
                        job_uuid = job['public_id']
                        max_runtime_in_seconds = self._root_job_wrapper['cloud_job']['max_runtime_in_seconds']
                        logger_no_user_data.debug(
                            f'Job "{job_uuid}" will have max run time set to {max_runtime_in_seconds} seconds'
                        )

                        try:
                            module_input_serialized = JobStorage.get_input(job=job)
                        except RetryException:
                            # Expect module input to be handled in a separate ModuleInput package
                            continue
                        except Exception as error:
                            raise error

                        JobMaxRuntimeTimerThread(
                            job_worker=self,
                            max_runtime_in_seconds=max_runtime_in_seconds,
                        ).start()

                        try:
                            self._run_root_job(module_input_serialized)

                        # This error occurs when trying to access the container after the job worker has cleaned it up.
                        # In that case stop the computation.
                        except DockerContainerNotFoundDuringExecutionException as err:
                            if self.is_cleaning_up:
                                break
                            else:
                                raise err

                elif package_type == 'ModuleInput':
                    if not self._root_job_wrapper:
                        raise Exception('No job saved yet')

                    try:
                        self._run_root_job(package)

                    # This error occurs when trying to access the container after the job worker has cleaned it up.
                    # In that case stop the computation.
                    except DockerContainerNotFoundDuringExecutionException as err:
                        if self.is_cleaning_up:
                            break
                        else:
                            raise err

                else:
                    logger_no_user_data.error('Package type from parent was not recognized')

                self._received_messages_queue.task_done()
            except ComputeProcessException:
                continue

            except Exception as exception:
                raise ComputeProcessException(
                    exception,
                    SystemExceptionCodes.UNKOWN_COMPUTE_PROCESS_ERROR.value,
                    self.send_system_exception
                ) from exception

    def _cleanup(self) -> None:
        self.is_cleaning_up = True

        for executor in self._executors:
            executor.cleanup()

        proxy_count = len(self._remote_host_proxies)
        if proxy_count > 0:
            proxy_cleanup_start_time = time()

            for proxy in self._remote_host_proxies:
                try:
                    proxy.terminate()
                except Exception as exception:  # pylint: disable=broad-except
                    logger_no_user_data.error('Failed to clean up remote host proxy')
                    logger.error(exception)

            self._remote_host_proxies = []
            logger_no_user_data.debug(f'Cleaned up {proxy_count} proxies in {time() - proxy_cleanup_start_time}')

        if self._dns_proxy:
            try:
                self._dns_proxy.remove(force=True)
                logger_no_user_data.debug('Cleaned up DNS Proxy')
            except Exception as exception:  # pylint: disable=broad-except
                logger_no_user_data.error('Failed to clean up DNS Proxy')
                logger.error(exception)

        self._cleanup_network(self._internal_network)
        self._internal_network = None
        self._cleanup_network(self._public_network)
        self._public_network = None

    @staticmethod
    def _cleanup_network(network: Optional[Network]) -> None:
        if network:
            network_cleanup_start_time = time()
            network_name = network
            try:
                network.remove()
            except Exception as exception:  # pylint: disable=broad-except
                logger_no_user_data.error(f'Failed to clean up {network_name}')
                logger.error(exception)

            logger_no_user_data.debug(f'Removed network {network_name} in {time() - network_cleanup_start_time}')

    def _handle_save_job_wrapper(self, package: bytes):
        job_wrapper_json_string = SavedJob(package).deserialize()
        job_wrapper: JobWrapper = json.loads(job_wrapper_json_string)
        BiolibApiClient.initialize(
            base_url=job_wrapper['BASE_URL'],
            access_token=job_wrapper['access_token']
        )
        self._root_job_wrapper = job_wrapper
        if not utils.IS_RUNNING_IN_CLOUD:
            job_wrapper['cloud_job'] = None

        self.job_temporary_dir = job_wrapper['job_temporary_dir']

        job = job_wrapper['job']
        self._jobs[job['public_id']] = job

        if job['app_version'].get('modules') is not None and BiolibDockerClient.is_docker_running():
            self._start_network_and_remote_host_proxies(job)

        # TODO: start downloading runtime zip already at this point

    def _start_network_and_remote_host_proxies(self, job: Job) -> None:
        app_version = job['app_version']
        job_id = job['public_id']
        remote_hosts = app_version['remote_hosts']

        for module in app_version['modules']:
            if module['environment'] == 'biolib-app' and module['name'] != 'main':
                remote_hosts.append(
                    {
                        'hostname': 'AppCallerProxy',
                    },
                )
                break

        docker_client = BiolibDockerClient.get_docker_client()
        try:
            self._internal_network = docker_client.networks.create(
                name=f'biolib-sandboxed-network-{job_id}',
                internal=True,
                driver='bridge',
            )
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_CREATE_DOCKER_NETWORKS.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception

        if len(remote_hosts) > 0:
            logger_no_user_data.debug(f'Job "{job_id}" creating networks for remote host proxies...')
            try:
                self._public_network = docker_client.networks.create(
                    name=f'biolib-proxy-network-{job_id}',
                    internal=False,
                    driver='bridge',
                )
            except Exception as exception:
                raise ComputeProcessException(
                    exception,
                    SystemExceptionCodes.FAILED_TO_CREATE_DOCKER_NETWORKS.value,
                    self.send_system_exception,
                    may_contain_user_data=False
                ) from exception
            logger_no_user_data.debug(f'Job "{job_id}" starting proxies for remote hosts: {remote_hosts}')
            try:
                hostname_to_ports: Dict[str, List[int]] = {}
                for remote_host in remote_hosts:
                    if ':' in remote_host['hostname']:
                        hostname, port_str = remote_host['hostname'].split(':')
                        port = int(port_str)
                    else:
                        port = 443
                        hostname = remote_host['hostname']

                    if hostname in hostname_to_ports:
                        hostname_to_ports[hostname].append(port)
                    else:
                        hostname_to_ports[hostname] = [port]

                for hostname, ports in hostname_to_ports.items():
                    remote_host_proxy = RemoteHostProxy(
                        RemoteHost(hostname=hostname),
                        self._public_network,
                        self._internal_network,
                        job_id,
                        ports
                    )
                    remote_host_proxy.start()
                    self._remote_host_proxies.append(remote_host_proxy)

                if utils.BIOLIB_ENABLE_DNS_PROXY:
                    domains_to_whitelist = list(hostname_to_ports.keys())
                    logger_no_user_data.debug(f'Job "{job_id}" starting DNS Proxy for domains: {domains_to_whitelist}')
                    self._start_dns_proxy(domains_to_whitelist=domains_to_whitelist)

            except Exception as exception:
                raise ComputeProcessException(
                    exception,
                    SystemExceptionCodes.FAILED_TO_START_REMOTE_HOST_PROXIES.value,
                    self.send_system_exception,
                    may_contain_user_data=False
                ) from exception

            logger_no_user_data.debug(f'Job "{job_id}" startup of remote host proxies completed')

    def _get_dns_proxy_image(self):
        docker = BiolibDockerClient.get_docker_client()
        try:
            return docker.images.get(_DNS_PROXY_IMAGE_URI)
        except ImageNotFound:
            logger_no_user_data.debug('Pulling DNS proxy Docker image...')
            return docker.images.pull(_DNS_PROXY_IMAGE_URI)

    def _start_dns_proxy(self, domains_to_whitelist):
        docker = BiolibDockerClient.get_docker_client()
        self._dns_proxy = docker.containers.create(
            detach=True,
            image=self._get_dns_proxy_image(),
            name=f'biolib-dns-proxy-{self._root_job_wrapper["job"]["public_id"]}',
            network=self._public_network.name,
        )

        blocky_config = '''
upstream:
    default:
        - 127.0.0.11
blocking:
    whiteLists:
        remoteHosts:
            - |'''
        for domain in domains_to_whitelist:
            blocky_config += f'''
              {domain}'''
        blocky_config += '''
    clientGroupsBlock:
        default:
            - remoteHosts
port: 53
'''

        blocky_config_bytes = blocky_config.encode()
        tarfile_in_memory = io.BytesIO()
        with tarfile.open(fileobj=tarfile_in_memory, mode='w:gz') as tar:
            info = tarfile.TarInfo('/config.yml')
            info.size = len(blocky_config_bytes)
            tar.addfile(info, io.BytesIO(blocky_config_bytes))

        tarfile_bytes = tarfile_in_memory.getvalue()
        tarfile_in_memory.close()
        docker.api.put_archive(self._dns_proxy.id, '/app', tarfile_bytes)

        self._internal_network.connect(self._dns_proxy.id)

        self._dns_proxy.start()

        proxy_is_ready = False
        for retry_count in range(1, 5):
            sleep(0.5 * retry_count)
            # Use the container logs as a health check.
            if b'TCP server is up and running' in self._dns_proxy.logs():
                proxy_is_ready = True
                break

        if not proxy_is_ready:
            self._dns_proxy.remove(force=True)
            raise Exception('DNS Proxy did not start properly')

        self._dns_proxy.reload()

    def _run_app_version(self, app_version_id: str, module_input_serialized: bytes, caller_job: Job) -> bytes:
        job: Job = BiolibJobApi.create(app_version_id, caller_job=caller_job['public_id'])
        self._jobs[job['public_id']] = job
        return self._run_job(job, module_input_serialized)

    def _run_job(self, job: Job, module_input_serialized: bytes) -> bytes:
        job_uuid = job['public_id']
        logger_no_user_data.info(f'Job "{job_uuid}" running...')
        if self._root_job_wrapper is None:
            raise Exception('root_job_wrapper was None')

        root_job = job
        while root_job['caller_job'] is not None and self._jobs.get(root_job['caller_job']) is not None:
            root_job = self._jobs[root_job['caller_job']]

        root_job_id = root_job['public_id']
        if job.get('arguments_override_command') and not job['app_version']['app']['allow_client_side_execution']:
            raise ComputeProcessException(
                Exception("Command override not allowed"),
                SystemExceptionCodes.COMMAND_OVERRIDE_NOT_ALLOWED.value,
                self.send_system_exception
            )

        modules = job['app_version'].get('modules')
        if not modules:
            raise ComputeProcessException(
                Exception("No modules found on job"),
                SystemExceptionCodes.NO_MODULES_FOUND_ON_JOB.value,
                self.send_system_exception
            )

        main_module = self._get_module_from_name(modules, module_name='main')

        source_files_are_mapped = False
        lfs_dict: Dict[str, LargeFileSystem] = {}
        for module in modules:
            if len(module['source_files_mappings']) > 0:
                source_files_are_mapped = True

            for lfs_mapping in module['large_file_systems']:
                logger_no_user_data.debug(f'Job "{job_uuid}" creating LFS for module "{module["name"]}"...')
                lfs = LargeFileSystem(
                    is_job_federated=job['federated_job_uuid'] is not None,
                    job_id=job['public_id'],
                    lfs_mapping=lfs_mapping,
                    send_status_update=self._send_status_update,
                )
                logger_no_user_data.debug(f'Job "{job_uuid}" created object for LFS "{lfs.uuid}"')

                lfs.initialize()
                lfs_dict[lfs.uuid] = lfs

        runtime_zip_bytes: Optional[bytes] = None
        if source_files_are_mapped:
            runtime_zip_bytes = self._get_runtime_zip_as_bytes(root_job_id=root_job_id, app_version=job['app_version'])

        module_output_serialized = self._run_module(
            LocalExecutorOptions(
                access_token=self._root_job_wrapper['access_token'],
                biolib_base_url=self._root_job_wrapper['BASE_URL'],
                compute_node_info=self._root_job_wrapper.get('compute_node_info'),
                internal_network=self._internal_network,
                job=job,
                cloud_job=self._root_job_wrapper['cloud_job'],
                large_file_systems=lfs_dict,
                module=main_module,
                remote_host_proxies=self._remote_host_proxies,
                root_job_id=root_job_id,
                dns_proxy=self._dns_proxy,
                runtime_zip_bytes=runtime_zip_bytes,
                send_status_update=self._send_status_update,
                send_system_exception=self.send_system_exception,
                send_stdout_and_stderr=self.send_stdout_and_stderr,
            ),
            module_input_serialized,
        )

        for lfs in lfs_dict.values():
            lfs.detach()

        if utils.IS_RUNNING_IN_CLOUD:
            # Log memory and disk after pulling and executing module
            log_disk_and_memory_usage_info()

        return module_output_serialized

    def _run_module(self, options: LocalExecutorOptions, module_input_serialized: bytes) -> bytes:
        module = options['module']
        executor_instance: BaseExecutor

        if module['environment'] == ModuleEnvironment.BIOLIB_APP.value:
            module_input = ModuleInput(module_input_serialized).deserialize()
            module_input_with_runtime_zip = self._add_runtime_zip_and_command_to_module_input(options, module_input)
            module_input_with_runtime_zip_serialized = ModuleInput().serialize(
                stdin=module_input_with_runtime_zip['stdin'],
                arguments=module_input_with_runtime_zip['arguments'],
                files=module_input_with_runtime_zip['files'],
            )
            return self._run_app_version(module['image_uri'], module_input_with_runtime_zip_serialized, options['job'])

        elif module['environment'] == ModuleEnvironment.BIOLIB_ECR.value and BiolibDockerClient.is_docker_running():
            executor_instance = DockerExecutor(options)

        elif module['environment'] == ModuleEnvironment.BIOLIB_ECR.value and \
                BiolibSingularityClient.is_singularity_running():
            executor_instance = SingularityExecutor(options)

        else:
            raise Exception(f"Unsupported module environment {module['environment']}")

        self._executors.append(executor_instance)

        if utils.IS_RUNNING_IN_CLOUD:
            # Log memory and disk before pulling and executing module
            log_disk_and_memory_usage_info()

        return executor_instance.execute_module(module_input_serialized)

    def _connect_to_parent(self):
        try:
            parent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            parent_socket.connect((SOCKET_HOST, int(self._socket_port)))

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_CONNECT_TO_WORKER_THREAD_SOCKET.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception

        try:
            SocketListenerThread(parent_socket, self._received_messages_queue).start()
            SocketSenderThread(parent_socket, self._messages_to_send_queue).start()
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_START_SENDER_THREAD_OR_RECEIVER_THREAD.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception

    # TODO: move this mapping logic to the ModuleInput class
    def _add_runtime_zip_and_command_to_module_input(self, options: LocalExecutorOptions, module_input):
        module = options['module']
        runtime_zip_byes = options['runtime_zip_bytes']
        # TODO: Figure out if we ever forward output mappings correctly (Do we only the mapping of the base image?)
        # TODO: Reuse much of the make_runtime_tar logic in BiolibDockerClient
        try:
            if runtime_zip_byes:
                runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_byes))
                source_mappings = Mappings(module['source_files_mappings'], module_input['arguments'])
                for zip_file_name in runtime_zip.namelist():
                    file_path = '/' + path_without_first_folder(zip_file_name)
                    mapped_file_names = source_mappings.get_mappings_for_path(file_path)
                    for mapped_file_name in mapped_file_names:
                        file_data = runtime_zip.read(zip_file_name)
                        module_input['files'].update({mapped_file_name: file_data})

            for command_part in reversed(shlex.split(module['command'])):
                module_input['arguments'].insert(0, command_part)

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_CREATE_NEW_JOB.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception

        return module_input

    def _get_runtime_zip_as_bytes(self, root_job_id: str, app_version: AppVersionOnJob) -> Optional[bytes]:
        runtime_zip_url = app_version['client_side_executable_zip']

        # TODO: change this to a is None check when backend is fixed to not return empty string
        if not runtime_zip_url:
            return None

        runtime_zip_bytes: Optional[bytes] = self._app_version_id_to_runtime_zip.get(app_version['public_id'])

        if runtime_zip_bytes is None:
            if root_job_id == utils.RUN_DEV_JOB_ID:
                with open(runtime_zip_url, mode='rb') as runtime_zip_file:
                    runtime_zip_bytes = runtime_zip_file.read()

            else:
                self._send_status_update(StatusUpdate(progress=25, log_message='Downloading Source Files...'))

                start_time = time()
                logger_no_user_data.debug(f'Job "{root_job_id}" downloading runtime zip...')
                try:
                    runtime_zip_bytes = requests.get(runtime_zip_url).content
                except Exception as exception:
                    raise ComputeProcessException(
                        exception,
                        SystemExceptionCodes.FAILED_TO_DOWNLOAD_RUNTIME_ZIP.value,
                        self.send_system_exception,
                        may_contain_user_data=False
                    ) from exception
                finally:
                    download_time = time() - start_time
                    logger_no_user_data.debug(f'Job "{root_job_id}" download of runtime zip took: {download_time}s')

            self._app_version_id_to_runtime_zip[app_version['public_id']] = runtime_zip_bytes

        return runtime_zip_bytes

    @staticmethod
    def _get_module_from_name(modules: List[Module], module_name: str):
        for module in modules:
            if module['name'] == module_name:
                return module
        raise Exception(f'Could not find module with name {module_name}')

    def send_system_exception(self, biolib_exception_code: int) -> None:
        system_exception_string = SystemExceptionCodeMap.get(biolib_exception_code)
        logger_no_user_data.error(f'Hit system exception: {system_exception_string} ({biolib_exception_code})')

        system_exception_package = SystemException().serialize(biolib_exception_code)
        self._messages_to_send_queue.put(system_exception_package)

    def send_stdout_and_stderr(self, stdout_and_stderr_bytes: bytes):
        stdout_and_stderr_package = StdoutAndStderr().serialize(
            stdout_and_stderr_bytes=stdout_and_stderr_bytes,
        )

        self._messages_to_send_queue.put(stdout_and_stderr_package)

    def _send_status_update(self, status_update: StatusUpdate) -> None:
        try:
            status_update_package = SystemStatusUpdate().serialize(
                status_update['progress'],
                status_update['log_message'],
            )
            logger.debug(status_update['log_message'])
            self._messages_to_send_queue.put(status_update_package)
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_SEND_STATUS_UPDATE.value,
                self.send_system_exception,
                may_contain_user_data=False
            ) from exception


    def _run_root_job(self, module_input_serialized):
        module_output_serialized = self._run_job(
            job=self._root_job_wrapper['job'],
            module_input_serialized=module_input_serialized,
        )

        module_output_size = len(module_output_serialized)
        job_uuid = self._root_job_wrapper['job']['public_id']
        logger_no_user_data.debug(
            f'Job "{job_uuid}" finished computation with module output size '
            f'of {module_output_size} bytes'
        )

        module_output_file_path = os.path.join(self.job_temporary_dir, "module_output.bbf")
        with open(module_output_file_path, 'wb') as module_output_file:
            module_output_file.write(module_output_serialized)

        self._send_status_update(StatusUpdate(progress=94, log_message='Computation finished'))
