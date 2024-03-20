# Changelog

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
