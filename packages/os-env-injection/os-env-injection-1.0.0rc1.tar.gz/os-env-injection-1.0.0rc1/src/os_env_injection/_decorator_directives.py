from typing import Optional


class Injection:
    def __init__(self, var_name: str, os_env_key: Optional[str] = None, is_required: bool = True):
        self._var_name = var_name
        self._os_env_key = os_env_key if os_env_key is not None else var_name
        self._required = is_required

    @property
    def var_name(self):
        return self._var_name

    @property
    def os_env_key(self):
        return self._os_env_key

    @property
    def required(self):
        return self._required
