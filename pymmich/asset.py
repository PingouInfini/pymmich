import json
import logging
from datetime import datetime, timezone
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError


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
                current_assets = [asset for asset in current_assets if asset.get('isExternal') == is_external]
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
        logging.error(f'Failed Downloading File with status code {response.status_code}')
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
        logging.error(f'Failed deleting assets with status code {response.status_code}')
        logging.error(response.text)
        return None
