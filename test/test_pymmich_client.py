import unittest
from datetime import datetime

from pymmich.client import PymmichClient
from pymmich.enums.asset_job import AssetJob
from pymmich.enums.job_name import JobName
from pymmich.enums.library_type import LibraryType

BASE_URL = "https://immich.mydomain.com"
API_KEY = "ABCDEFGHIJKLMNOPQRZTUVWXYZ0123456789"


class TestPymmichClient(unittest.TestCase):
    def setUp(self):
        self.client = PymmichClient(base_url=BASE_URL, api_key=API_KEY)

    def check_if_asset_is_correct(self, asset):
        expected_asset_keys = {
            'id', 'deviceAssetId', 'ownerId', 'deviceId', 'libraryId', 'type', 'originalPath', 'originalFileName',
            'resized', 'thumbhash', 'fileCreatedAt', 'fileModifiedAt', 'localDateTime', 'updatedAt', 'isFavorite',
            'isArchived', 'isTrashed', 'duration', 'exifInfo', 'livePhotoVideoId', 'people', 'checksum', 'stackCount',
            'isOffline', 'hasMetadata', 'duplicateId'
        }
        self.assertTrue(expected_asset_keys.issubset(asset.keys()))

    def check_if_album_is_correct(self, album):
        expected_album_keys = {
            'albumName', 'description', 'albumThumbnailAssetId', 'createdAt', 'updatedAt', 'id', 'ownerId', 'owner',
            'albumUsers', 'shared', 'hasSharedLink', 'startDate', 'endDate', 'assets', 'assetCount',
            'isActivityEnabled', 'order'
        }
        expected_owner_keys = {'id', 'email', 'name', 'profileImagePath', 'avatarColor'}
        expected_user_keys = {'user', 'role'}
        expected_user_sub_keys = {'id', 'email', 'name', 'profileImagePath', 'avatarColor'}

        self.assertIsInstance(album, dict, "One of the albums is not a dictionary")
        self.assertTrue(expected_album_keys.issubset(album.keys()), "The album does not contain all the expected keys")
        self.assertTrue(expected_owner_keys.issubset(album['owner'].keys()),
                        "The 'owner' object does not contain all the expected keys")
        for album_user in album['albumUsers']:
            self.assertTrue(expected_user_keys.issubset(album_user.keys()),
                            "One of the 'albumUsers' does not contain all the expected keys")
            self.assertTrue(expected_user_sub_keys.issubset(album_user['user'].keys()),
                            "The 'user' object in 'albumUsers' does not contain all the expected keys")

    def check_if_job_is_correct(self, job):
        expected_job_keys = {
            'jobCounts', 'queueStatus'
        }
        expected_job_counts_keys = {'active', 'completed', 'failed', 'delayed', 'waiting', 'paused'}
        expected_queue_status_keys = {'isActive', 'isPaused'}

        self.assertIsInstance(job, dict, "One of the jobs is not a dictionary")
        self.assertTrue(expected_job_keys.issubset(job.keys()), "The album does not contain all the expected keys")
        self.assertTrue(expected_job_counts_keys.issubset(job['jobCounts'].keys()),
                        "The 'jobCounts' object does not contain all the expected keys")
        self.assertTrue(expected_queue_status_keys.issubset(job['queueStatus'].keys()),
                        "The 'queueStatus' object does not contain all the expected keys")

    ###################################################################################################################
    # ALBUM
    ###################################################################################################################
    def test_get_all_albums(self):
        response = self.client.album.get_albums(asset_id=None, shared_album=None)

        self.assertIsInstance(response, list, "Response is not a list")
        for album in response:
            self.check_if_album_is_correct(album)

    def test_get_all_shared_albums(self):
        response = self.client.album.get_albums(asset_id=None, shared_album=True)

        self.assertIsInstance(response, list, "Response is not a list")
        for album in response:
            self.check_if_album_is_correct(album)

    def test_get_all_unshared_albums(self):
        response = self.client.album.get_albums(asset_id=None, shared_album=False)

        self.assertIsInstance(response, list, "Response is not a list")
        for album in response:
            self.check_if_album_is_correct(album)

    def test_get_specific_album(self):
        random_asset = self.client.asset.get_random()
        response = self.client.album.get_albums(asset_id=random_asset[0].get('id'))

        self.assertIsInstance(response, list, "Response is not a list")

        for album in response:
            self.check_if_album_is_correct(album)

    def test_get_album_by_id(self):
        # without id
        response = self.client.album.get_album(album_id=None)
        self.assertEqual(response, None)
        response = self.client.album.get_album_by_id(album_id=None)
        self.assertEqual(response, None)

        # with id
        all_albums = self.client.album.get_albums(asset_id=None, shared_album=True)
        response = self.client.album.get_album(album_id=all_albums[0].get('id'))
        self.check_if_album_is_correct(response)

        response = self.client.album.get_album_by_id(album_id=all_albums[0].get('id'))
        self.check_if_album_is_correct(response)

    def test_get_album_by_name(self):
        all_albums = self.client.album.get_albums(asset_id=None, shared_album=True)
        response = self.client.album.get_album_by_name(target_album_name=all_albums[0].get('albumName'))
        self.check_if_album_is_correct(response)

    def test_actions_on_test_album(self):
        test_album_name = "TEST_album"

        # create_album
        user_test = self.client.user.get_my_user()
        response = self.client.album.create_album(test_album_name, [user_test.get('id')])
        test_album = self.client.album.get_album_by_name(target_album_name=test_album_name)
        self.assertTrue(response)

        # add_assets_to_album
        random_asset = self.client.asset.get_random()
        response = self.client.album.add_assets_to_album(test_album.get('id'), [random_asset[0].get('id')])
        self.assertTrue(response)
        assets_album = self.client.album.get_albums(asset_id=random_asset[0].get('id'))
        assert any(album.get('albumName') == 'TEST_album' for album in
                   assets_album), "No album with 'albumName' == 'TEST_album' found"

        # delete_album
        response = self.client.album.delete_album(test_album.get('id'))
        self.assertTrue(response)

    ###################################################################################################################
    # ASSET
    ###################################################################################################################
    def test_get_random(self):
        count = 3
        response = self.client.asset.get_random(count=count)
        self.assertEqual(len(response), count)
        self.assertIsInstance(response, list, "Response is not a list")
        for asset in response:
            self.check_if_asset_is_correct(asset)

    def test_get_all_user_assets_by_device_id(self):
        response = self.client.asset.get_all_user_assets_by_device_id(device_id="Library Import")
        self.assertIsInstance(response, list, "Response is not a list")
        assert all(isinstance(item, str) for item in response), "response does not only contain strings"

    def test_get_full_sync_for_user(self):
        client_id = self.client.user.get_my_user().get('id')
        response = self.client.asset.get_full_sync_for_user(user_id=client_id,
                                                            updated_after=datetime.strptime('2024-01-01T01:23:45.678Z',
                                                                                            '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                            limit=1, is_external=True)
        self.assertIsInstance(response, list, "Response is not a list")
        for asset in response:
            self.check_if_asset_is_correct(asset)

    def test_get_asset_info(self):
        random_asset = self.client.asset.get_random()
        response = self.client.asset.get_asset_info(random_asset[0].get('id'))
        self.check_if_asset_is_correct(response)

    def test_download_asset(self):
        random_asset = self.client.asset.get_random()
        response = self.client.asset.download_asset(random_asset[0].get('id'))
        self.assertIsNotNone(response, "the response must be neither None nor False")

    def test_upload_and_delete_assets(self):  # TODO
        # upload
        pass
        # delete
        pass

    def test_view_asset(self):
        random_asset = self.client.asset.get_random()
        response = self.client.asset.view_asset(random_asset[0].get('id'))
        self.assertIsNotNone(response)

    def test_run_asset_jobs(self):
        random_asset = self.client.asset.get_random()
        response = self.client.asset.run_asset_jobs([random_asset[0].get('id')], AssetJob.REFRESH_METADATA)
        self.assertTrue(response)

    ###################################################################################################################
    # Job
    ###################################################################################################################
    def test_send_job_command(self):
        response = self.client.job.send_job_command(JobName.SIDECAR)
        self.check_if_job_is_correct(response)

    def test_get_all_jobs_status(self):
        response = self.client.job.get_all_jobs_status()
        for job in response:
            self.assertIsNotNone(job)

    def test_get_job_status(self):
        response = self.client.job.get_job_status(JobName.SIDECAR)
        self.check_if_job_is_correct(response)

    ###################################################################################################################
    # Library
    ###################################################################################################################
    def test_get_libraries(self):
        expected_keys = {
            'id', 'ownerId', 'name', 'createdAt', 'updatedAt', 'refreshedAt', 'assetCount',
            'importPaths', 'exclusionPatterns'
        }
        response = self.client.library.get_libraries()
        self.assertIsInstance(response, list, "Response is not a list")
        for library in response:
            self.assertTrue(expected_keys.issubset(library.keys()))

        response = self.client.library.get_libraries(LibraryType.EXTERNAL)
        self.assertIsInstance(response, list, "Response is not a list")
        for library in response:
            self.assertTrue(expected_keys.issubset(library.keys()))

    def test_scan_library(self):
        library = self.client.library.get_libraries()[0]
        response = self.client.library.scan_library(library.get('id'))
        self.assertTrue(response)

    def test_remove_offline_files(self):
        library = self.client.library.get_libraries()[0]
        response = self.client.library.remove_offline_files(library.get('id'))
        self.assertTrue(response)

    ###################################################################################################################
    # USER
    ###################################################################################################################
    def test_get_my_user(self):
        expected_keys = {
            'id', 'email', 'name', 'profileImagePath', 'avatarColor', 'storageLabel', 'shouldChangePassword',
            'isAdmin', 'createdAt', 'deletedAt', 'updatedAt', 'oauthId', 'quotaSizeInBytes', 'quotaUsageInBytes',
            'status'
        }
        response = self.client.user.get_my_user()
        self.assertTrue(expected_keys.issubset(response.keys()))

    def test_get_user(self):
        user_test = self.client.user.get_my_user()
        expected_keys = {
            'id', 'email', 'name', 'profileImagePath', 'avatarColor'
        }
        response = self.client.user.get_user(user_test.get('id'))
        self.assertTrue(expected_keys.issubset(response.keys()))

    def test_get_user_by_id(self):
        user_test = self.client.user.get_my_user()
        expected_keys = {
            'id', 'email', 'name', 'profileImagePath', 'avatarColor'
        }
        response = self.client.user.get_user_by_id(user_test.get('id'))
        self.assertTrue(expected_keys.issubset(response.keys()))


if __name__ == '__main__':
    unittest.main()
