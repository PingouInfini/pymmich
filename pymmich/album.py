import json
import logging

import requests

from pymmich.user import get_user


def get_album(self, album_id=None) -> object:
    logging.debug(f"### Get album with id : {album_id}")

    if album_id is None:
        logging.debug(f"### Response album : None")
        return None

    url = f"{self.base_url}/api/albums/{album_id}"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response album : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve album {album_id} with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_album_by_name(self, target_album_name, albums=None) -> object:
    logging.debug(f"### Get album by name : {target_album_name}")
    if not albums:
        curr_album = get_albums(self)
    else:
        curr_album = albums

    for album in curr_album:
        if album.get('albumName') == target_album_name:
            logging.debug(f"### Returned album : {album}")
            return album

    logging.debug(f"### Returned album : None")
    return None


def get_albums(self, asset_id=None, shared_album=None) -> object:
    logging.debug(f"### Get albums with asset_id : {asset_id} and shared_album : {shared_album}")

    url = f"{self.base_url}/api/albums"

    if asset_id is not None and shared_album is None:
        url = f"{self.base_url}/api/albums?assetId={asset_id}"
    elif asset_id is None and shared_album is True:
        url = f"{self.base_url}/api/albums?shared=true"
    elif asset_id is None and shared_album is False:
        url = f"{self.base_url}/api/albums?shared=false"
    elif asset_id is not None and shared_album is True:
        url = f"{self.base_url}/api/albums?assetId={asset_id}&shared=true"
    elif asset_id is not None and shared_album is False:
        url = f"{self.base_url}/api/albums?assetId={asset_id}&shared=false"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response albums : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve albums with asset_id : {asset_id} and shared_album : {shared_album}'
                      f' with status code {response.status_code}')
        logging.error(response.text)
        return None


def create_album(self, album_name, owners_id) -> bool:
    logging.debug("### Album creation name '" + album_name + "' for users " + str(
        [get_user(self, user_id).get('name') for user_id in owners_id if get_user(self, user_id)]))

    url = f'{self.base_url}/api/albums'

    # Creates a list of dictionaries for albumUsers
    album_users = [{"role": "editor", "userId": user_id} for user_id in owners_id]

    # Creates JSON payload with data
    payload = {
        "albumName": album_name,
        "albumUsers": album_users
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.post(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code in (200, 201):
        logging.debug('Album creation successful')
        return True
    else:
        logging.error(f'Album {album_name} creation failed with status code {response.status_code}')
        logging.error(response.text)
        return False


def delete_album(self, album_id) -> bool:
    logging.debug(f"### Delete album with album_id : {album_id}")

    url = f'{self.base_url}/api/albums/{album_id}'

    # Creates JSON payload with data
    payload = {}

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.delete(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Delete album done")
        return True
    else:
        logging.error(f'Failed deleting album {album_id} with status code {response.status_code}')
        logging.error(response.text)
        return False


def add_assets_to_album(self, album_id, assets_ids) -> bool:
    logging.debug("### Add in album " + album_id + " : " + str(len(assets_ids)) + " assets")

    url = f'{self.base_url}/api/albums/{album_id}/assets'

    # Creates JSON payload with data
    payload = {
        "ids": list(assets_ids)
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.put(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code in (200, 201):
        logging.debug('Add assets to album successful')
        return True
    else:
        logging.error(f'Add assets to album {album_id} failed with status code {response.status_code}')
        logging.error(response.text)
        return False
