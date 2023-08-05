import logging
import os
import sys
import random
import subprocess
import threading
import time
import pathlib

import requests.exceptions

from biolib import utils
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_binary_format import ModuleOutput
from biolib.biolib_docker_client import BiolibDockerClient
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger
from biolib.biolib_singularity_client import BiolibSingularityClient
from biolib.compute_node.job_worker.executors import RemoteExecutor, RemoteExecuteOptions
from biolib.utils import stream_process_output
from biolib.typing_utils import Optional


# TODO: type return value as ModuleOutput class
def run_job(job, module_input_serialized: bytes):
    job_id = job['public_id']
    modules = job['app_version'].get('modules')
    logger.info(f'Job "{job_id}" is starting...')

    # Run in remote (in cloud)
    if modules is None or utils.BIOLIB_FORCE_REMOTE_COMPUTE or not utils.BASE_URL_IS_PUBLIC_BIOLIB or (
            not BiolibDockerClient.is_docker_running() and not BiolibSingularityClient.is_singularity_running()
    ):
        result = RemoteExecutor.execute_job(
            RemoteExecuteOptions(
                biolib_base_url=utils.BIOLIB_BASE_URL,
                job=job,
                root_job_id=job_id,
            ),
            module_input_serialized,
        )
        return ModuleOutput(result).deserialize()

    # Run locally
    host = '127.0.0.1'
    port = str(random.choice(range(5000, 65000)))
    node_url = f'http://{host}:{port}'
    logger.debug(f'Starting local compute node at {node_url}')
    start_cli_path = pathlib.Path(__file__).parent.parent.resolve() / 'start_cli.py'
    python_executable_path = sys.executable
    output_destination: Optional[int]
    if utils.IS_RUNNING_IN_NOTEBOOK:
        utils.STREAM_STDOUT = True
        output_destination = subprocess.PIPE
    elif utils.STREAM_STDOUT:
        # If not running in notebook but streaming stdout is enabled (probably running as CLI)
        # set output destination to None to have it write to current process output (this does not work in notebook)
        output_destination = None
    else:
        output_destination = subprocess.DEVNULL

    compute_node_process = subprocess.Popen(
        args=[python_executable_path, start_cli_path, 'start', '--host', host, '--port', port],
        env=dict(
            os.environ,
            BIOLIB_LOG=logging.getLevelName(logger.level),
            BIOLIB_BASE_URL=BiolibApiClient.get().base_url
        ),
        stdout=output_destination,
        stderr=output_destination,
    )

    if utils.IS_RUNNING_IN_NOTEBOOK:
        logger.debug('Running in Notebook, so starting output streaming thread...')
        threading.Thread(target=stream_process_output, args=(compute_node_process,)).start()

    try:
        for retry in range(20):
            time.sleep(1)
            try:
                BiolibJobApi.save_compute_node_job(
                    job=job,
                    module_name='main',
                    access_token=BiolibApiClient.get().access_token,
                    node_url=node_url
                )
                break

            except requests.exceptions.ConnectionError:
                if retry == 19:
                    raise BioLibError('Could not connect to local compute node') from None
                logger.debug('Could not connect to local compute node retrying...')

        BiolibJobApi.start_cloud_job(job_id, module_input_serialized, node_url)
        BiolibJobApi.await_compute_node_status(
            retry_interval_seconds=1.5,
            retry_limit_minutes=43800,  # Let users run an app locally for a month (43800 minutes)
            status_to_await='Result Ready',
            compute_type='Compute Node',
            node_url=node_url,
            job=job,
        )

        result = BiolibJobApi.get_cloud_result(job_id, node_url)
        return ModuleOutput(result).deserialize()

    finally:
        compute_node_process.terminate()
