from biolib import utils
from biolib.biolib_api_client import BiolibApiClient, Job
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_binary_format import ModuleInput, EncryptedModuleOutputWithKey
from biolib.biolib_binary_format.utils import RemoteIndexableBuffer
from biolib.biolib_binary_format.unencrypted_module_output import UnencryptedModuleOutput
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.biolib_logging import logger_no_user_data, logger


class JobStorage:

    @staticmethod
    def upload_module_input(job: Job, module_input_serialized: bytes) -> None:
        base_url = BiolibApiClient.get().base_url
        job_uuid = job['public_id']
        headers = {'Job-Auth-Token': job['auth_token']}

        multipart_uploader = utils.MultiPartUploader(
            start_multipart_upload_request=dict(
                requires_biolib_auth=True,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/start_upload/',
                headers=headers
            ),
            get_presigned_upload_url_request=dict(
                requires_biolib_auth=True,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/presigned_upload_url/',
                headers=headers
            ),
            complete_upload_request=dict(
                requires_biolib_auth=True,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/complete_upload/',
                headers=headers
            ),
        )

        multipart_uploader.upload(
            payload_iterator=utils.get_chunk_iterator_from_bytes(module_input_serialized),
            payload_size_in_bytes=len(module_input_serialized),
        )

    @staticmethod
    def upload_module_output(job_uuid: str, module_output: bytes, aes_key_string_b64: str) -> None:
        try:
            if not aes_key_string_b64:
                storage_module_output = UnencryptedModuleOutput.create_from_serialized_module_output(module_output)
                logger_no_user_data.debug(f'Job "{job_uuid}" uploading result to S3...')

            else:
                storage_module_output = EncryptedModuleOutputWithKey(
                    aes_key_string_b64=aes_key_string_b64
                ).create_from_serialized_module_output(module_output)
                logger_no_user_data.debug(f'Job "{job_uuid}" uploading encrypted result to S3...')

        except Exception as error:
            logger_no_user_data.debug('Failed to get storage module output from serialized module output')
            logger.debug(f'Failed to get storage module output from serialized module output due to {error}')
            raise error

        # Free up memory as quickly as possible
        del module_output

        base_url = BiolibApiClient.get().base_url
        config = CloudUtils.get_webserver_config()
        compute_node_auth_token = config['compute_node_info']['auth_token']  # pylint: disable=unsubscriptable-object
        headers = {'Compute-Node-Auth-Token': compute_node_auth_token}

        multipart_uploader = utils.MultiPartUploader(
            start_multipart_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/start_upload/',
                headers=headers,
            ),
            get_presigned_upload_url_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/presigned_upload_url/',
                headers=headers,
            ),
            complete_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/complete_upload/',
                headers=headers,
            ),
        )

        multipart_uploader.upload(
            payload_iterator=utils.get_chunk_iterator_from_bytes(storage_module_output),
            payload_size_in_bytes=len(storage_module_output),
        )

    @staticmethod
    def get_module_input(job: Job) -> bytes:
        presigned_download_url = BiolibJobApi.get_job_storage_download_url(job=job, storage_type='input')
        buffer = RemoteIndexableBuffer(url=presigned_download_url)
        return ModuleInput().convert_to_serialized_module_input(buffer)

    @staticmethod
    def get_module_output(job: Job) -> bytes:
        presigned_download_url = BiolibJobApi.get_job_storage_download_url(job=job, storage_type='results')

        buffer = RemoteIndexableBuffer(url=presigned_download_url)
        unencrypted_module_output = UnencryptedModuleOutput(buffer)
        return unencrypted_module_output.convert_to_serialized_module_output()
