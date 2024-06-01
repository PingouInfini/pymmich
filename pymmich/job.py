import json
import logging

import requests

from pymmich.enums.job_name import JobName


def get_all_jobs_status(self) -> object:
    logging.debug(f"### Get all jobs status")

    url = f"{self.base_url}/api/jobs"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response all jobs status : {response.json()}")
        return response.json()
    else:
        logging.error(f'Failed to retrieve all jobs status with status code {response.status_code}')
        logging.error(response.text)
        return None


def get_job_status(self, job_name: JobName) -> object:
    logging.debug(f"### Get job '{job_name}' status ")

    url = f"{self.base_url}/api/jobs"

    response = requests.get(url, **self.requests_kwargs, verify=True)

    if response.status_code == 200:
        logging.debug(f"### Response job status : {response.json()}")
        return response.json().get(job_name)
    else:
        logging.error(f'Failed to retrieve job status with status code {response.status_code}')
        logging.error(response.text)
        return None


def send_job_command(self, job_command: JobName, force: bool = False) -> object:
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
