from typing import Tuple, Optional

import pytest

from os_env_injection import inject_os_env, Injection, OSEnvInjectionError


@pytest.mark.parametrize(
    "args_and_kwargs",
    [
        ((None, None, 1, 2), dict()),
        ((None, None, 1), {"y": 2}),
        ((None, None), {"x": 1, "y": 2}),
        ((None,), {"var2": None, "x": 1, "y": 2}),
        (tuple(), {"var1": None, "var2": None, "x": 1, "y": 2}),
    ],
)
def test_if_2_optional_injected_os_env_and_values_are_not_passed_and_no_os_env_then_return_none(
    args_and_kwargs: Tuple[tuple, dict]
):
    assert f_2_optional_os_env(*args_and_kwargs[0], **args_and_kwargs[1]) == (None, None, 1, 2)


@inject_os_env(
    injections=[
        Injection(var_name="var1", os_env_key="var1", is_required=False),
        Injection(var_name="var2", os_env_key="var2", is_required=False),
    ]
)
def f_2_optional_os_env(
    var1: Optional[str], var2: Optional[str], x: object, y: object
) -> Tuple[str, str, object, object]:
    return var1, var2, x, y


@pytest.mark.parametrize(
    "args_and_kwargs",
    [
        ((None, None, 1, 2), dict()),
        ((None, None, 1), {"y": 2}),
        ((None, None), {"x": 1, "y": 2}),
        ((None,), {"var2": None, "x": 1, "y": 2}),
        (tuple(), {"var1": None, "var2": None, "x": 1, "y": 2}),
    ],
)
def test_if_1_optional_1_required_injected_os_env_and_values_are_not_passed_and_no_os_env_then_raise_exception(
    args_and_kwargs: Tuple[tuple, dict]
):
    with pytest.raises(OSEnvInjectionError):
        f_1_os_env_1_optional_os_env(*args_and_kwargs[0], **args_and_kwargs[1])


@inject_os_env(
    injections=[
        Injection(var_name="var1", os_env_key="var1", is_required=True),
        Injection(var_name="var2", os_env_key="var2", is_required=False),
    ]
)
def f_1_os_env_1_optional_os_env(
    var1: str, var2: Optional[str], x: object, y: object
) -> Tuple[str, str, object, object]:
    return var1, var2, x, y
