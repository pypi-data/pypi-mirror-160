import base64

from databutton.utils import is_running_locally

from .apiclient import get_remote
from .local import get_local


def get(key: str) -> str:
    """Get project secret with specified key.

    Secrets stored in the cloud are only available when running in the cloud.
    When running locally, the local secrets file is inspected instead.

    If the secret is not found, a KeyError exception is raised.
    """
    secret = get_local(key) if is_running_locally() else get_remote(key)
    if secret is None:
        raise KeyError(f"Secret {key} was not found in this project.")
    return secret


def get_hex(key: str) -> bytes:
    """Get a project secret and decode it from hex format to raw bytes."""
    return bytes.fromhex(get(key))


def get_base64(key: str) -> bytes:
    """Get a project secret and decode it from base64 format to raw bytes."""
    # Note: This handles both standard and urlsafe base64 variants just fine
    return base64.urlsafe_b64decode(get(key))
