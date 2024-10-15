import json
import logging

import requests

from pymmich.enums.library_type import LibraryType


def get_libraries(self, library_type: LibraryType = None) -> object:
    logging.debug(f"### Get libraries with library_type : {library_type}")

    if not library_type:
        url = f'{self.base_url}/api/libraries'
    else:
        url = f'{self.base_url}/api/libraries?type={library_type.name}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response libraries : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve libraries {library_type} with status code {response.status_code}')
        logging.error(response.text)
        return None


def scan_library(self, library_id, refresh_all_files=None, refresh_modified_files=None) -> bool:
    logging.debug(f"### Scan library with library_id : {library_id} and refresh_all_files : {refresh_all_files} "
                  f"and refresh_modified_files : {refresh_modified_files}")

    url = f'{self.base_url}/api/libraries/{library_id}/scan'

    # Creates JSON payload with data
    if refresh_all_files is None and refresh_modified_files is None:
        payload = {}
    else:
        payload = {
            "refreshAllFiles": refresh_all_files if refresh_all_files is not None else False,
            "refreshModifiedFiles": refresh_modified_files if refresh_modified_files is not None else False
        }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.post(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 204:
        logging.debug(f"### Scan library done")
        return True
    else:
        logging.error(f'Failed scanning library {library_id} with status code {response.status_code}')
        logging.error(response.text)
        return False