import logging
from datetime import datetime, timezone

import requests


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
