import os
from typing import Optional, Tuple

from os_env_injection import inject_os_env, Injection


def test_if_os_env_key_is_specified_then_value_is_taken_from_it():
    os.environ["OS_VAR"] = "foo"
    assert f() == "foo"
    del os.environ["OS_VAR"]


@inject_os_env(injections=[Injection(var_name="var", os_env_key="OS_VAR", is_required=True)])
def f(var: str) -> str:
    return var


def test_if_os_env_key_is_not_specified_then_value_is_taken_from_its_os_env_with_var_name():
    os.environ["var"] = "foo"
    assert f_no_os_env_key() == "foo"
    del os.environ["var"]


@inject_os_env(injections=[Injection(var_name="var")])
def f_no_os_env_key(var: str) -> str:
    return var


def test_complex_scenario():
    os.environ["OS_VAR1"] = "foo"
    os.environ["OS_VAR2"] = "jam"
    assert complex_f(
        None,
        1,
        var2=None,
    ) == ("foo", 1, "jam", None, 3)
    del os.environ["OS_VAR1"]
    del os.environ["OS_VAR2"]


@inject_os_env(
    injections=[
        Injection(var_name="var1", os_env_key="OS_VAR1", is_required=True),
        Injection(var_name="var2", os_env_key="OS_VAR2", is_required=True),
        Injection(var_name="var3", os_env_key="var3", is_required=False),
    ]
)
def complex_f(
    var1: str, x: int, var2: str = "spam", var3: Optional[str] = None, y: int = 3
) -> Tuple[str, int, str, str, int]:
    return var1, x, var2, var3, y
