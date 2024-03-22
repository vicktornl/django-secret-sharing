# Changelog

## [0.8.0] - [UNRELEASED]

- Add official support for Django 4.1, 4.2 and 5.0
- Add official support for Python 3.11 and 3.12
- Fix: Catch and return 404 when the sharing url is invalid
- Drop support for Django 2.2, 3.0, 3.1, and 3.2
- Drop support for Python 3.6 and 3.7

## [0.7.0] - 2022-12-08

- Fix: allow s3 client overrides via settings (e.g. for testing locally with s3)

## [0.6.0] - 2022-12-06

- Added: `delete_stale_files` management command to delete stale files
- fix: include credentials for basic auth protected backends

## [0.5.0] - 2022-09-30

### Added

- Cryptography for AES encryption
- Support for Django 4 and Python 3.10

### Removed

- Pycrypto as it's no longer maintained
- Support for Django 2.x

[0.5.0]: https://github.com/vicktornl/django-secret-sharing/compare/0.4.0...0.5.0
