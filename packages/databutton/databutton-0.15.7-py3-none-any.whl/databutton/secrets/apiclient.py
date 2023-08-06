import os
from typing import Optional

import requests

from databutton.utils import get_api_url, get_auth_token, get_databutton_config

# TODO: Need to get a better grasp on error handling and response codes etc.


class SecretsApiClient:
    def __init__(self, project_id: str):
        self.base_url = get_api_url(project_id) + "/secrets"
        self.project_id = project_id

    def _headers(self):
        token = get_auth_token()
        if token is None or token == "":
            raise EnvironmentError(
                "Missing auth token. Are you logged in to databutton?"
            )
        return {
            "Authorization": f"Bearer {token}",
            "x-databutton-release": os.environ.get("DATABUTTON_RELEASE"),
            "x-project-id": self.project_id,  # TODO: rename to x-databutton-project-id everywhere else then remove
            "x-databutton-project-id": self.project_id,
        }

    def add(self, key: str, value: str) -> bool:
        res = requests.post(
            self.base_url + "/add",
            headers=self._headers(),
            json={"key": key, "value": value},
        )
        if not res.ok:
            raise Exception("Failed to add secret")
        return res.json()["key"] == key

    def get(self, key: str) -> str:
        res = requests.post(  # Yes, it's post, to pass parameters in json body
            self.base_url + "/get",
            headers=self._headers(),
            json={"key": key},
        )
        if not res.ok:
            raise Exception("Failed to read secret")
        return res.json()["value"]

    def delete(self, key: str) -> bool:
        res = requests.post(
            self.base_url + "/delete",
            headers=self._headers(),
            json={"key": key},
        )
        if not res.ok:
            raise Exception("Failed to delete secret")
        return res.json()["key"] == key

    def list(self) -> list[str]:
        res = requests.get(
            self.base_url + "/list",
            headers=self._headers(),
        )
        if not res.ok:
            raise Exception("Failed to list secrets")
        return res.json()["secrets"]


def get_remote(key: str) -> Optional[str]:
    config = get_databutton_config()
    client = SecretsApiClient(config.uid)
    return client.get(key)
