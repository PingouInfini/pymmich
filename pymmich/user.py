import logging

import requests


def get_my_user(self) -> object:
    logging.debug(f"### Get my user")

    url = f'{self.base_url}/api/users/me'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response user : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve my user with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_user(self, user_id) -> object:
    logging.debug(f"### Get user with id : {user_id}")

    url = f'{self.base_url}/api/users/{user_id}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response user : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve user with id {user_id} with status code {response.status_code}')
        logging.error(response.text)
        return None
