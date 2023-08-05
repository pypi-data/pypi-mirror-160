import os
from typing import Optional


def read_var_from_os_env_if_not_provided(os_env_key: str, value: Optional[str] = None, required: bool = False) -> str:
    if value is None:
        result = os.environ.get(os_env_key, None)
    else:
        result = value

    if result is None and required:
        raise OSEnvInjectionError(os_env_key=os_env_key)

    return result


class OSEnvInjectionError(Exception):
    def __init__(self, os_env_key: str):
        self._os_env_key = os_env_key

    def __str__(self):
        return f"OS env variable {self._os_env_key} not found, and passed value is None"
