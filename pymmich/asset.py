import json
import logging
from datetime import datetime, timezone
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError

from pymmich.enums.asset_job import AssetJob


def get_assets(self, is_external=None, updated_after: datetime = None):
    logging.debug(f"### Get assets with is_external : {is_external} and updatedAfter : {updated_after}")

    assets = []
    number_of_assets_to_fetch_per_request = 100
    skip = 0

    while True:
        url = f'{self.base_url}/api/asset?take={number_of_assets_to_fetch_per_request}&skip={skip}'

        if updated_after:
            # Converts updated_after to UTC if its timezone is not already UTC
            if updated_after.tzinfo is not None and updated_after.tzinfo.utcoffset(updated_after) is not None:
                updated_after = updated_after.astimezone(timezone.utc)
            else:
                updated_after = updated_after.replace(tzinfo=timezone.utc)

            url += f'&updatedAfter={updated_after.strftime("%Y-%m-%d %H:%M:%S")}'

        response = requests.get(url, **self.requests_kwargs, verify=True)

        if response.status_code == 200:
            current_assets = response.json()
            if is_external is not None:
                current_assets = [asset for asset in current_assets
                                  if asset.get('originalPath').startswith("/usr/src/app/external")]
            assets.extend(current_assets)

            if len(response.json()) < number_of_assets_to_fetch_per_request:
                break
            else:
                skip += number_of_assets_to_fetch_per_request

        else:
            logging.error(f'Failed to retrieve assets with status code {response.status_code}')
            logging.error(response.text)
            return None

    logging.debug(f"### Response assets : {assets}")
    return assets


def get_asset_info(self, asset_id) -> object:
    logging.debug(f"### Get asset '{asset_id}' info")

    url = f"{self.base_url}/api/asset/{asset_id}"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response asset info status : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve asset {asset_id} info status with status code {response.status_code}')
        logging.error(response.text)
        return None


def download_file(self, asset_id) -> object:
    logging.debug(f"### Download File with asset_id : {asset_id}")

    url = f'{self.base_url}/api/download/asset/{asset_id}'

    response = requests.post(url, **self.requests_kwargs, verify=True)

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
            return None
        finally:
            image_bytes.close()  # Ensure the stream is always closed
            del image_bytes
    else:
        logging.error(f'Failed Downloading File {asset_id} with status code {response.status_code}')
        logging.error(response.text)
        return None


def delete_assets(self, assets_ids) -> None:
    logging.debug(f"### Delete assets with assets_ids : {assets_ids}")

    url = f'{self.base_url}/api/asset'

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
        return None
    else:
        logging.error(f'Failed deleting assets {assets_ids} with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_asset_thumbnail(self, asset_id) -> object:
    logging.debug(f"### Get asset thumbnail with asset_id : {asset_id}")

    url = f'{self.base_url}/api/asset/thumbnail/{asset_id}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response asset thumbnail : {response.content}")
        return response.content
    else:
        logging.error(f'Failed to retrieve asset {asset_id} thumbnail with status code {response.status_code}')
        logging.error(response.text)
        return None


def run_asset_jobs(self, assets_ids, asset_job: AssetJob = AssetJob.REGENERATE_THUMBNAIL) -> None:
    logging.debug(f"### Run asset jobs with assets_ids : {assets_ids} and asset_job : {asset_job}")

    url = f'{self.base_url}/api/asset/jobs'

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
        return None
    else:
        logging.error(f'Failed running asset jobs with assets_ids : {assets_ids} and asset_job : {asset_job} '
                      f'with status code {response.status_code}')
        logging.error(response.text)
        return None
