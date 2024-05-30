import json
import logging

import requests

from pymmich.enums.job_command import JobCommand


def send_job_command(self, job_command: JobCommand, force: bool = False) -> object:
    logging.debug(f"### Send job command with job_command : {job_command}")

    if job_command is None:
        return

    url = f'{self.base_url}/api/jobs/{job_command}'

    # Creates JSON payload with data
    payload = {
        "command": "start",
        "force": force
    }

    # Converts payload to JSON
    payload = json.dumps(payload)

    response = requests.put(url, data=payload, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Send job command : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to send job command with status code {response.status_code}')
        logging.error(response.text)
        return None
