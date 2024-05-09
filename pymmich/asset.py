import logging

import requests


def get_assets(self, is_external=None, updated_after=None):
    logging.debug(f"### Get assets with is_external : {is_external} and updatedAfter : {updated_after}")

    url = f'{self.base_url}/api/asset'

    if updated_after:
        url = f'{self.base_url}/api/asset?updatedAfter={updated_after}'

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        assets = response.json()
        if is_external is not None and is_external:
            assets = [asset for asset in assets if asset.get('isExternal') is True]
        elif is_external is not None and not is_external:
            assets = [asset for asset in assets if asset.get('isExternal') is False]
        logging.debug(f"### Response assets : {assets}")
        return assets
    else:
        logging.error(f'Failed to retrieve assets with status code {response.status_code}')
        logging.error(response.text)
        return None
