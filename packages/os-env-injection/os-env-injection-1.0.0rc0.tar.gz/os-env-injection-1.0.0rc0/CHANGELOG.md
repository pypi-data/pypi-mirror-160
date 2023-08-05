# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## MAJOR
### Added
* `Injection`s, which are used to specify the behavior of `inject_os_env`, instead of the unclear dictionary
### Changed
* Type hints will not be used to infer OS env key and if a value is required to be `None` or not
* `OSError` is replaced by `OSEnvInjectionError` when a value is not passed (`None`) and OS env variable is missing

## 0.0.1
### Added
* proper `README` with examples

## 0.0.0
### Added
* `inject_os_env` decorator, that automatically inject OS env variables
* introduce the type `Injection`, which can be used to notify to the decorator `inject_os_env` which variables are to be injected
