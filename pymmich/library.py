import json
import logging

import requests

from pymmich.enums.library_type import LibraryType


def get_libraries(self, library_type: LibraryType = None) -> object:
    logging.debug(f"### Get libraries with library_type : {library_type}")

    if not library_type:
        url = f'{self.base_url}/api/library'
    else:
        url = f'{self.base_url}/api/library?type={library_type.name}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response libraries : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve libraries with status code {response.status_code}')
        logging.error(response.text)
        return None


def scan_library(self, library_id, refresh_all_files=False, refresh_modified_files=True) -> object:
    logging.debug(f"### Scan library with library_id : {library_id} and refresh_all_files : {refresh_all_files} "
                  f"and refresh_modified_files : {refresh_modified_files}")

    url = f'{self.base_url}/api/library/{library_id}/scan'

    # Creates JSON payload with data
    payload = {
        "refreshAllFiles": refresh_all_files,
        "refreshModifiedFiles": refresh_modified_files
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.post(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 204:
        logging.debug(f"### Scan library done")
        return None
    else:
        logging.error(f'Failed scanning library with status code {response.status_code}')
        logging.error(response.text)
        return None


def remove_offline_files(self, library_id) -> None:
    logging.debug(f"### Remove Offline Files with library_id : {library_id}")

    url = f'{self.base_url}/api/library/{library_id}/removeOffline'

    response = requests.post(url, **self.requests_kwargs, verify=True)

    if response.status_code == 204:
        logging.debug(f"### Remove offline files done")
        return None
    else:
        logging.error(f'Failed remove offline files with status code {response.status_code}')
        logging.error(response.text)
        return None
