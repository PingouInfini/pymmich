import logging

import requests


def get_assets(self, is_external=None, updated_after=None):
    logging.debug(f"### Get assets with is_external : {is_external} and updatedAfter : {updated_after}")

    assets = []
    number_of_assets_to_fetch_per_request = 100
    skip = 0

    while True:
        url = f'{self.base_url}/api/asset?take={number_of_assets_to_fetch_per_request}&skip={skip}'

        if updated_after:
            updated_after = updated_after.strftime("%Y-%m-%d %H:%M:%S")
            url += f'&updatedAfter={updated_after}'

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
