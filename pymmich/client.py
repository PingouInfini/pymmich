""" Python wrapper for the Immich API """
from pymmich import album, asset, library, user, job
from pymmich.enums.asset_job import AssetJob
from pymmich.enums.job_name import JobName
from pymmich.enums.library_type import LibraryType


class AlbumClient:
    def __init__(self, parent_client):
        self.parent_client = parent_client

    def get_album(self, album_id=None) -> object:
        return album.get_album(self.parent_client, album_id)

    def get_album_by_id(self, album_id=None) -> object:
        return album.get_album(self.parent_client, album_id)

    def get_album_by_name(self, target_album_name, albums=None) -> object:
        return album.get_album_by_name(self.parent_client, target_album_name, albums)

    def get_albums(self, asset_id=None, shared_album=None) -> object:
        return album.get_albums(self.parent_client, asset_id, shared_album)

    def create_album(self, album_name, owners_id) -> bool:
        return album.create_album(self.parent_client, album_name, owners_id)

    def delete_album(self, album_id) -> bool:
        return album.delete_album(self.parent_client, album_id)

    def add_assets_to_album(self, album_id, assets_ids) -> bool:
        return album.add_assets_to_album(self.parent_client, album_id, assets_ids)


class AssetClient:
    def __init__(self, parent_client):
        self.parent_client = parent_client

    def get_random(self, count=1) -> object:
        return asset.get_random(self.parent_client, count)

    def get_all_user_assets_by_device_id(self, device_id) -> object:
        return asset.get_all_user_assets_by_device_id(self.parent_client, device_id)

    def get_full_sync_for_user(self, user_id, last_asset_id=None, updated_until=None, updated_after=None, limit=100,
                               is_external: bool = False) -> object:
        return asset.get_full_sync_for_user(self.parent_client, user_id, last_asset_id, updated_until, updated_after,
                                            limit, is_external)

    def get_asset_info(self, asset_id) -> object:
        return asset.get_asset_info(self.parent_client, asset_id)

    def download_asset(self, asset_id) -> object:
        return asset.download_asset(self.parent_client, asset_id)

    def delete_assets(self, assets_ids) -> bool:
        return asset.delete_assets(self.parent_client, assets_ids)

    def view_asset(self, asset_id) -> object:
        return asset.view_asset(self.parent_client, asset_id)

    def run_asset_jobs(self, assets_ids, asset_job: AssetJob = AssetJob.REGENERATE_THUMBNAIL) -> bool:
        return asset.run_asset_jobs(self.parent_client, assets_ids, asset_job)


class JobClient:
    def __init__(self, parent_client):
        self.parent_client = parent_client

    def get_all_jobs_status(self) -> object:
        return job.get_all_jobs_status(self.parent_client)

    def get_job_status(self, job_name: JobName) -> object:
        return job.get_job_status(self.parent_client, job_name)

    def send_job_command(self, job_command: JobName, force: bool = False) -> object:
        return job.send_job_command(self.parent_client, job_command, force)


class LibraryClient:
    def __init__(self, parent_client):
        self.parent_client = parent_client

    def get_libraries(self, library_type: LibraryType = None) -> object:
        return library.get_libraries(self.parent_client, library_type)

    def scan_library(self, library_id, refresh_all_files=None, refresh_modified_files=None) -> bool:
        return library.scan_library(self.parent_client, library_id, refresh_all_files, refresh_modified_files)


class UserClient:
    def __init__(self, parent_client):
        self.parent_client = parent_client

    def get_my_user(self) -> object:
        return user.get_my_user(self.parent_client)

    def get_user(self, user_id) -> object:
        return user.get_user(self.parent_client, user_id)

    def get_user_by_id(self, user_id) -> object:
        return user.get_user(self.parent_client, user_id)


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

        self.album = AlbumClient(self)
        self.asset = AssetClient(self)
        self.job = JobClient(self)
        self.library = LibraryClient(self)
        self.user = UserClient(self)

    async def __aenter__(self):
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            tb
    ) -> None:
        pass
