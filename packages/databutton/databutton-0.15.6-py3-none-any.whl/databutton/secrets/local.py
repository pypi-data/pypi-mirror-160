from typing import Optional

import yaml

from databutton.utils import get_project_directory

LOCAL_SECRETS_FILENAME = "secrets.yaml"


def read_local_secrets() -> dict:
    secrets_filename = get_project_directory() / LOCAL_SECRETS_FILENAME
    try:
        # Could also support a secrets directory with
        # files named as keys and containing the values,
        # that's what we'll do for the docker mounting thing?
        with open(secrets_filename, "r") as f:
            secrets = yaml.safe_load(f)
        return secrets or {}
    except FileNotFoundError:
        return {}


_local_secrets = None


def get_local(key: str) -> Optional[str]:
    global _local_secrets
    if _local_secrets is None:
        _local_secrets = read_local_secrets()
    return _local_secrets.get(key)


def _clear_local_secrets_cache():
    global _local_secrets
    _local_secrets = None
