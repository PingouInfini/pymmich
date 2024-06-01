""" Python wrapper for the Immich API """
from pymmich import album, asset, library, user, job
from pymmich.enums.asset_job import AssetJob
from pymmich.enums.job_name import JobName
from pymmich.enums.library_type import LibraryType


class PymmichClient:
    """Interface class"""
    base_url: str
    api_key: str
    requests_kwargs: object

    def __init__(
            self,
            base_url: str,
            api_key: str,
    ) -> None:
        """
        Constructor

        :param base_url: the root API URL of immich, e.g. https://immich.mydomain.com/
        :param api_key: the Immich API Key to use
        """

        self.base_url = base_url
        self.api_key = api_key
        self.requests_kwargs = {
            'headers': {
                'x-api-key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }

    async def __aenter__(self):
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            tb
    ) -> None:
        pass

    ###################################################################################################################
    # ALBUM
    ###################################################################################################################

    def get_album(self, album_id=None) -> object:
        return album.get_album(self, album_id)

    def get_album_by_id(self, album_id=None) -> object:
        return album.get_album(self, album_id)

    def get_album_by_name(self, target_album_name, albums=None) -> object:
        return album.get_album_by_name(self, target_album_name, albums)

    def get_albums(self, asset_id=None, shared_album=None) -> object:
        return album.get_albums(self, asset_id, shared_album)

    def create_album(self, album_name, owners_id) -> None:
        return album.create_album(self, album_name, owners_id)

    def add_assets_to_album(self, album_id, assets_ids) -> None:
        return album.add_assets_to_album(self, album_id, assets_ids)

    ###################################################################################################################
    # ASSET
    ###################################################################################################################

    def get_assets(self, is_external=None, updated_after=None) -> object:
        return asset.get_assets(self, is_external, updated_after)

    def download_file(self, asset_id) -> object:
        return asset.download_file(self, asset_id)

    def delete_assets(self, assets_ids) -> None:
        return asset.delete_assets(self, assets_ids)

    def get_asset_thumbnail(self, asset_id) -> object:
        return asset.get_asset_thumbnail(self, asset_id)

    def run_asset_jobs(self, assets_ids, asset_job: AssetJob = AssetJob.REGENERATE_THUMBNAIL) -> None:
        return asset.run_asset_jobs(self, assets_ids, asset_job)

    ###################################################################################################################
    # LIBRARY
    ###################################################################################################################

    def get_libraries(self, library_type: LibraryType = None) -> object:
        return library.get_libraries(self, library_type)

    def scan_library(self, library_id, refresh_all_files=None, refresh_modified_files=None) -> object:
        return library.scan_library(self, library_id, refresh_all_files, refresh_modified_files)

    def remove_offline_files(self, library_id) -> None:
        return library.remove_offline_files(self, library_id)

    ###################################################################################################################
    # USER
    ###################################################################################################################

    def get_user_by_id(self, user_id) -> object:
        return user.get_user_by_id(self, user_id)

    ###################################################################################################################
    # JOB
    ###################################################################################################################

    def get_all_jobs_status(self) -> object:
        return job.get_all_jobs_status(self)

    def get_job_status(self, job_name: JobName) -> object:
        return job.get_job_status(self, job_name)

    def send_job_command(self, job_command: JobName, force: bool = False) -> object:
        return job.send_job_command(self, job_command, force)
