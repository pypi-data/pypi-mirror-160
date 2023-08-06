import logging
import subprocess

from docker.errors import ImageNotFound, APIError  # type: ignore

from biolib import utils
from biolib.biolib_docker_client import BiolibDockerClient
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger_no_user_data
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.compute_node.job_worker.cache_state import DockerImageCacheState, DockerCacheStateError
from biolib.compute_node.job_worker.cache_types import DockerImageInfo, DockerImageCacheStateDict, DockerAuthConfig, \
    UuidStr


class DockerImageCache:
    def __init__(self):
        if not utils.IS_RUNNING_IN_CLOUD:
            raise BioLibError('Using DockerImageCache outside Cloud is not supported')

        config = CloudUtils.get_webserver_config()
        self._max_cache_size = config['max_docker_image_cache_size_bytes']  # pylint: disable=unsubscriptable-object
        self._docker_client = BiolibDockerClient().get_docker_client()
        self._docker_data_dir = self._docker_client.info()['DockerRootDir']

    def _get_current_docker_data_usage_in_bytes(self) -> int:
        disk_usage_command = ['df', self._docker_data_dir]
        logger_no_user_data.debug(f'Running {disk_usage_command}...')
        df_output = subprocess.run(
            disk_usage_command,
            capture_output=True,
            check=True,
            timeout=3,
        ).stdout.decode()
        logger_no_user_data.debug(df_output)
        df_output_lines = [s.split() for s in df_output.splitlines()]

        # Expect the filesystem to be row 1 and expect column 2 to be used disk space
        return int(df_output_lines[1][2])

    def _clear_space_for_image(self, estimated_image_size_bytes: int, cache_state: DockerImageCacheStateDict):
        for _ in range(100):
            if not self._has_space_to_pull_image(estimated_image_size_bytes, cache_state):
                self._remove_least_recently_used_image(cache_state)
            else:
                return

        raise DockerCacheStateError('Failed to free space for Docker image')

    def get(self, image_uri: str, estimated_image_size_bytes: int,
            pull_auth_config: DockerAuthConfig, job_id: str) -> None:
        try:
            with DockerImageCacheState() as cache_state:
                if image_uri not in cache_state:
                    raise ImageNotFound('Image not found in cache')

                self._docker_client.images.get(image_uri)
                cache_state[image_uri]['last_used_at'] = DockerImageCacheState.get_timestamp_now()
                cache_state[image_uri]['active_jobs'].append(job_id)

        except ImageNotFound:
            if estimated_image_size_bytes > self._max_cache_size:
                logger_no_user_data.error(
                    f'Image {image_uri} with size: {estimated_image_size_bytes} is bigger than the max cache size'
                )
                raise DockerCacheStateError(  # pylint: disable=raise-missing-from
                    'Image is bigger than the max cache size'
                )

            with DockerImageCacheState() as cache_state:
                if not self._has_space_to_pull_image(estimated_image_size_bytes, cache_state):
                    self._clear_space_for_image(estimated_image_size_bytes, cache_state)

                cache_state[image_uri] = DockerImageInfo(
                    last_used_at=DockerImageCacheState.get_timestamp_now(),
                    uri=image_uri,
                    state='pulling',
                    estimated_image_size_bytes=estimated_image_size_bytes,
                    active_jobs=[job_id]
                )

            logger_no_user_data.debug(f'Image {image_uri} not found in cache. Pulling...')
            try:
                self._docker_client.images.pull(image_uri, auth_config=pull_auth_config)
            except Exception as error:
                logger_no_user_data.error(f'Could not pull image due to {error}')

                # Remove image from cache_state
                with DockerImageCacheState() as cache_state:
                    if image_uri in cache_state:
                        cache_state.pop(image_uri)

                raise error

            with DockerImageCacheState() as cache_state:
                cache_state[image_uri]['state'] = 'ready'

    @staticmethod
    def detach_job(image_uri: str, job_id: UuidStr) -> None:
        try:
            with DockerImageCacheState() as cache_state:
                if image_uri in cache_state and job_id in cache_state[image_uri]['active_jobs']:
                    cache_state[image_uri]['active_jobs'].remove(job_id)

        except Exception as error:  # pylint: disable=broad-except
            logging.error('Could not remove job from image cache')
            logging.error(error)

    def _remove_least_recently_used_image(self, cache_state: DockerImageCacheStateDict) -> None:
        cached_images = [image for image in cache_state.values() if image['state'] == 'ready']
        images_sorted_by_least_recently_used = sorted(cached_images, key=lambda image: image['last_used_at'])

        for image in images_sorted_by_least_recently_used:
            logger_no_user_data.debug(f"Removing image: {image['uri']}")

            # Only remove images that has no active jobs
            if image['active_jobs']:
                logger_no_user_data.debug(
                    f"Skipping removal of image {image['uri']} as it has the active jobs {image['active_jobs']}"
                )
                continue

            try:
                self._docker_client.api.remove_image(image=image['uri'])
            except APIError as error:
                logger_no_user_data.error(
                    f'Could not remove image due to {error}... Skipping removal of this image.'
                )
                continue  # Image is in use or cannot be removed at this time

            cache_state.pop(image['uri'])
            break

    def _has_space_to_pull_image(self, estimated_image_size_bytes: int, cache_state: DockerImageCacheStateDict) -> bool:
        logger_no_user_data.debug('Calculating cache metrics...')
        size_of_images_being_pulled = sum([image['estimated_image_size_bytes'] for image in cache_state.values()
                                           if image['state'] == 'pulling'])
        stored_cached_size = self._get_current_docker_data_usage_in_bytes()
        current_cache_size = stored_cached_size + size_of_images_being_pulled

        cache_space_remaining = self._max_cache_size - current_cache_size
        logger_no_user_data.debug(f'Cache remaining: {cache_space_remaining}. Needed: {estimated_image_size_bytes}.')
        logger_no_user_data.debug(f'Stored: {stored_cached_size}. Pulling: {size_of_images_being_pulled}')

        return bool(cache_space_remaining > estimated_image_size_bytes)
