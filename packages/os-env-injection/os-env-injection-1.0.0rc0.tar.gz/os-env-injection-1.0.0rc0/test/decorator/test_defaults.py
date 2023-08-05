import os
from typing import Optional

from os_env_injection import inject_os_env, Injection


def test_if_var_is_let_to_default_none_value_then_value_comes_from_os_env():
    os.environ["var"] = "foo"
    assert f_default_none() == "foo"
    del os.environ["var"]


@inject_os_env(injections=[Injection(var_name="var", os_env_key="var", is_required=False)])
def f_default_none(var: Optional[str] = None) -> str:
    return var


def test_if_var_is_let_to_default_value_then_value_comes_from_it():
    assert f_default_spam() == "spam"


def test_if_var_is_let_to_default_value_then_value_comes_from_it_despite_os_env():
    os.environ["var"] = "foo"
    assert f_default_spam() == "spam"


@inject_os_env(injections=[Injection(var_name="var", os_env_key="var", is_required=True)])
def f_default_spam(var: str = "spam") -> str:
    return var
