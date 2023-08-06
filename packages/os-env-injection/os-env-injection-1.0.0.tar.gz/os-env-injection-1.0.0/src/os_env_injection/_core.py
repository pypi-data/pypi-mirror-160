import os
from typing import Optional


def inject_var(var_value: Optional[str], os_env_key: str, is_required: bool = True) -> str:
    if var_value is None:
        result = os.environ.get(os_env_key, None)
    else:
        result = var_value

    if result is None and is_required:
        raise OSEnvInjectionError(os_env_key=os_env_key)

    return result


class OSEnvInjectionError(Exception):
    def __init__(self, os_env_key: str):
        self._os_env_key = os_env_key

    def __str__(self):
        return f"OS env variable {self._os_env_key} not found, and passed value is None"
