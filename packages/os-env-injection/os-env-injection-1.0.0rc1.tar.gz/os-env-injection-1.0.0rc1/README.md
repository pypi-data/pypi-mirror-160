# os-env-injection
Utilities to handle OS environment variables

## Why this library?

You have a function which requires several arguments that typically depend on the system on when the function is running
```python
def f(url: str, user: str, password: str, subdomain: str):
    ...
```

You would like to have the possibility to have its values to be read from the OS env, so that, at will, you could invoke 
it as
```python
f()
```

If you simply write
```python
import os

def f(
    url: str = os.environ["URL"],
    user: str = os.environ["USER"],
    password: str = os.environ["PASSWORD"],
    subdomain: str = os.environ["SUBDOMAIN"],
):
    ...
```
then you will encounter a problem whenever the OS env variables are not set, because the defaults are evaluated at import time.
This means in practice, that you will be forced to use them, instead of passing the values directly.

A workaround is
```python
import os

def f(
    url: str = os.environ.get("URL", None),
    user: str = os.environ.get("USER", None),
    password: str = os.environ.get("PASSWORD", None),
    subdomain: str = os.environ.get("SUBDOMAIN", None),
):
    ...
```
In this way, there are still a couple of drawbacks:
* it is necessary to write code to check the values of each variable to raise an exception if values are missing (`None`)
* the default values will be evaluated when the function is first imported.   
  In case you are setting the OS env dynamically (e.g. by executing a shell script with `export`s) you could end up in troubles.



## The nice solution - Quickstart

First, install the library
```shell
pip install os-env-injection
```

From the previous example, say that all variables are required except for `subdomain` which can stay `None`.
You can leverage on this library in two ways, depending on your favorite style.

#### Imperative style

```python
from os_env_injection import inject_var


def f(url: str | None, user: str | None, password: str | None, subdomain: str | None) -> None:
    url = inject_var(var_value=url, os_env_key="OS_ENV_URL")
    user = inject_var(var_value=user, os_env_key="OS_ENV_USER")
    password = inject_var(var_value=password, os_env_key="OS_ENV_PASSWORD")
    subdomain = inject_var(var_value=subdomain, os_env_key="OS_ENV_SUBDOMAIN", is_required=False)
    ...
```

**Note**: `inject_var(var_value=url, os_env_key="OS_ENV_URL")` is the same as `inject_var(var_value=url, os_env_key="OS_ENV_URL", is_required=True)`.


#### Functional style

```python
from os_env_injection import inject_os_env, Injection


@inject_os_env(
    injections=[
        Injection(var_name="url", os_env_key="OS_ENV_URL"),
        Injection(var_name="user", os_env_key="OS_ENV_USER"),
        Injection(var_name="password", os_env_key="OS_ENV_PASSWORD"),
        Injection(var_name="subdomain", os_env_key="OS_ENV_SUBDOMAIN", is_required=False),
    ]
)
def f(url: str, user: str, password: str, subdomain: str | None) -> None:
    ...
```

**Note**: `Injection(var_name="url")` is the same as `Injection(var_name="url", os_env_key="url", is_required=True)`.


#### What will happen?

* If you explicitly pass a value when you call `f`, it will be used
* If no value is passed, then it will try to read it from the OS environment variable specified in `os_env_key`. 
* If no value is passed nor found in the OS environment, then it will raise an exception if `is_required` is `True`.
  Else it will not raise an exception and set the value to `None` otherwise.


## Setup development environment (for contributors only)

* Create a virtual environment and activate it
  ```shell
  python -m venv venv
  source venv/bin/activate
  ```

* Install the developer dependencies you will need
  ```shell
  pip install -U pip wheel setuptools
  pip install -e .[dev]
  ```
  
* Set black as pre-commit package (will automatically apply [black](https://github.com/psf/black) before committing)
  ```shell
  pre-commit install
  ```
  
* To run the tests
  ```shell
  pytest
  ```
