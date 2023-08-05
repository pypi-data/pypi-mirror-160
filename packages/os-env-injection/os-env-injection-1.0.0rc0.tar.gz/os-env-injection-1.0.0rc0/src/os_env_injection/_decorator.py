import inspect
from functools import wraps
from typing import Callable, Dict, Iterable

from os_env_injection._core import read_var_from_os_env_if_not_provided
from os_env_injection._decorator_directives import Injection


def inject_os_env(injections: Iterable[Injection] = None) -> Callable:
    def inject(f: Callable) -> Callable:
        @wraps(f)
        def inject_f(*args, **kwargs):
            kwargs = _turn_args_into_kwargs(args, kwargs)
            kwargs = _integrate_with_os_env(kwargs=kwargs)
            return f(**kwargs)

        def _turn_args_into_kwargs(args: tuple, kwargs: Dict[str, object]) -> Dict[str, object]:
            kwargs_complement = {
                k: args[i]
                for i, k in enumerate(inspect.getfullargspec(f).args)
                if k not in kwargs.keys() and i < len(args)
            }
            kwargs.update(kwargs_complement)
            return kwargs

        def _integrate_with_os_env(kwargs: dict) -> Dict[str, object]:
            kw_defaults = _extract_f_defaults()
            for v in injections:
                kwargs[v.var_name] = read_var_from_os_env_if_not_provided(
                    os_env_key=v.os_env_key,
                    value=kwargs.get(v.var_name, kw_defaults.get(v.var_name, None)),
                    required=v.required,
                )
            return kwargs

        def _extract_f_defaults() -> Dict[str, object]:
            if inspect.getfullargspec(f).defaults is None:
                kw_defaults = dict()
            else:
                kw_defaults = {
                    arg: default
                    for arg, default in zip(
                        inspect.getfullargspec(f).args[::-1], inspect.getfullargspec(f).defaults[::-1]
                    )
                }
            return kw_defaults

        return inject_f

    return inject
