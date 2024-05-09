import logging

import requests


def get_user_by_id(self, user_id):
    logging.debug(f"### Get user with id : {user_id}")

    url = f'{self.base_url}/api/user/info/{user_id}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response user : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve user by id with status code {response.status_code}')
        logging.error(response.text)
        return None
