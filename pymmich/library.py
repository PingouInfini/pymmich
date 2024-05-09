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
