import os
from datetime import timedelta

import pytest
from django.utils import timezone

from django_secret_sharing.utils import (
    ENCODING,
    IV_LENGTH,
    KEY_LENGTH,
    create_secret,
    decrypt_value,
    encrypt_value,
    get_date_by_expires_value,
    get_key_iv_pair,
    get_secret_by_url_part,
)

ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24
ONE_WEEK = 60 * 60 * 24 * 7


def test_key_iv_pair():
    key, iv = get_key_iv_pair()

    assert len(key) == KEY_LENGTH
    assert key.__class__ == bytes

    assert len(iv) == IV_LENGTH
    assert iv.__class__ == bytes


@pytest.mark.parametrize(
    "value",
    [
        "Hellö, : World!",
        "This is a longer value than the first one.",
        "1",
        ":!.@#$%^&*()",
    ],
)
def test_encrypt_and_decrypt(value):
    key, iv = get_key_iv_pair()

    encrypted, value_length = encrypt_value(value, key, iv)
    decrypted = decrypt_value(encrypted, value_length, key, iv)

    assert decrypted == value


@pytest.mark.django_db
def test_create_secret():
    raw_value = "My secret value"
    secret, url_part = create_secret(value=raw_value)
    assert not secret.erased
    assert secret.value != raw_value
    assert str(secret.id) not in url_part


@pytest.mark.django_db
def test_get_secret():
    raw_value = "My secret value"
    secret, url_part = create_secret("My secret value")
    secret, value = get_secret_by_url_part(url_part)
    assert not secret.erased
    assert secret.value != value
    assert value == raw_value


def test_get_date_by_expires_value():

    one_hour = get_date_by_expires_value(expires_value=ONE_HOUR)
    one_day = get_date_by_expires_value(expires_value=ONE_DAY)
    seven_days = get_date_by_expires_value(expires_value=ONE_WEEK)
    unused_value = get_date_by_expires_value(expires_value="1 year secret")

    assert (timezone.now() + timedelta(hours=1)).hour == one_hour.hour
    assert (timezone.now() + timedelta(days=1)).day == one_day.day
    assert (timezone.now() + timedelta(days=7)).day == seven_days.day
    assert not unused_value
