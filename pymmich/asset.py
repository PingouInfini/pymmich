import json
import logging
from datetime import datetime, timezone
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError

from pymmich.enums.asset_job import AssetJob


def get_all_user_assets_by_device_id(self, device_id) -> object:
    logging.debug(f"### Get all user assets with device_id : {device_id}")

    url = f"{self.base_url}/api/assets/device/{device_id}"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response all user assets : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve all user assets with device_id : {device_id} '
                      f'with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_full_sync_for_user(self, user_id, last_asset_id=None, updated_until=None, updated_after=None, limit=100,
                           is_external: bool = False) -> object:
    logging.debug(f"### Get full sync for user with user_id : {user_id}, last_asset_id : {last_asset_id}, "
                  f"updated_until : {updated_until}, updated_after : {updated_after}, limit : {limit} and "
                  f"is_external : {is_external}")

    if not updated_until:
        updated_until = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    try:
        datetime.strptime(updated_until, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        raise ValueError(f"The updated_until parameter '{updated_until}' does not respect the expected format "
                         f"'%Y-%m-%dT%H:%M:%S.%fZ'")

    if updated_after is not None:
        # Converts updated_after to UTC if its timezone is not already UTC
        if updated_after.tzinfo is not None and updated_after.tzinfo.utcoffset(updated_after) is not None:
            updated_after = updated_after.astimezone(timezone.utc)
        else:
            updated_after = updated_after.replace(tzinfo=timezone.utc)

    url = f'{self.base_url}/api/sync/full-sync'

    # Creates JSON payload with data
    payload = {
        "lastId": last_asset_id,
        "limit": limit,
        "updatedUntil": updated_until,
        "userId": user_id
    }

    if last_asset_id is None:
        del payload["lastId"]

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.post(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        response_data = response.json()
        if updated_after is not None:
            response_data = [item for item in response_data if
                             datetime.strptime(item['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                                 tzinfo=timezone.utc) >= updated_after]
        if is_external:
            response_data = [item for item in response_data if item['originalPath'].startswith('/usr/src/app/external')]

        return response_data
    else:
        logging.error(f'Failed with status code {response.status_code}')
        logging.error(response.text)


def get_random(self, count=1) -> object:
    logging.debug(f"### Get random asset with count : {count}")

    url = f"{self.base_url}/api/assets/random?count={count}"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response random asset : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve random asset with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_asset_info(self, asset_id) -> object:
    logging.debug(f"### Get asset '{asset_id}' info")

    url = f"{self.base_url}/api/assets/{asset_id}"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response asset info status : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve asset {asset_id} info status with status code {response.status_code}')
        logging.error(response.text)
        return None


def download_asset(self, asset_id) -> object:
    logging.debug(f"### Download File with asset_id : {asset_id}")

    url = f'{self.base_url}/api/assets/{asset_id}/original'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200 and 'image/' in response.headers.get('Content-Type', ''):
        logging.debug(f"### Download File done")
        image_bytes = BytesIO(response.content)
        try:
            image = Image.open(image_bytes)
            image.load()  # Force loading the image data while the file is open
            image_bytes.close()  # Now we can safely close the stream
            return image
        except UnidentifiedImageError:
            print(
                f"Failed to identify image for asset_id {asset_id}. Content-Type: {response.headers.get('Content-Type')}")
            image_bytes.close()  # Ensure the stream is closed even if an error occurs
            return False
        finally:
            image_bytes.close()  # Ensure the stream is always closed
            del image_bytes
    else:
        logging.error(f'Failed Downloading File {asset_id} with status code {response.status_code}')
        return False


def delete_assets(self, assets_ids) -> bool:
    logging.debug(f"### Delete assets with assets_ids : {assets_ids}")

    url = f'{self.base_url}/api/assets'

    # Creates JSON payload with data
    payload = {
        "force": True,
        "ids": list(assets_ids)
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.delete(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 204:
        logging.debug(f"### Delete assets done")
        return True
    else:
        logging.error(f'Failed deleting assets {assets_ids} with status code {response.status_code}')
        logging.error(response.text)
        return False


def view_asset(self, asset_id) -> object:
    logging.debug(f"### Get asset thumbnail with asset_id : {asset_id}")

    url = f'{self.base_url}/api/assets/{asset_id}/thumbnail'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response asset thumbnail : {response.content}")
        return response.content
    else:
        logging.error(f'Failed to retrieve asset {asset_id} thumbnail with status code {response.status_code}')
        logging.error(response.text)
        return None


def run_asset_jobs(self, assets_ids, asset_job: AssetJob = AssetJob.REGENERATE_THUMBNAIL) -> bool:
    logging.debug(f"### Run asset jobs with assets_ids : {assets_ids} and asset_job : {asset_job}")

    url = f'{self.base_url}/api/assets/jobs'

    # Creates JSON payload with data
    payload = {
        "name": asset_job,
        "assetIds": list(assets_ids)
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.post(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 204:
        logging.debug(f"### Run asset jobs done")
        return True
    else:
        logging.error(f'Failed running asset jobs with assets_ids : {assets_ids} and asset_job : {asset_job} '
                      f'with status code {response.status_code}')
        logging.error(response.text)
        return False
