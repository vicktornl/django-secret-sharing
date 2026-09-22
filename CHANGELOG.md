# Changelog

## [0.8.0] - 2026-09-22

### Changed

- Added support for Django 5.2, 6.0, and 6.1
- Added support for Python 3.12, 3.13, 3.14, and 3.15

## Removed

- Dropped support for Django versions earlier than 5.2
- Dropped support for Python 3.7, 3.8, 3.9, and 3.10

### Fixed

- Catch ValueError too when get_secret_by_url_part raises an exception (#15)

## [0.7.0] - 2022-12-08

### Added

- Add `AWS_ENDPOINT_URL`, `AWS_USE_SSL`, `AWS_VERIFY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SIGNATURE_VERSION` Django settings for configuring the AWS S3 storage backend.

## [0.6.0] - 2022-12-06

### Added

- Add `delete_stale_files` management command.

## [0.5.0] - 2022-09-30

### Added

- Cryptography for AES encryption
- Support for Django 4 and Python 3.10

### Removed

- Pycrypto as it's no longer maintained
- Support for Django 2.x

[0.5.0]: https://github.com/vicktornl/django-secret-sharing/compare/0.4.0...0.5.0
