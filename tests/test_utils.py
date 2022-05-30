from datetime import timedelta

import pytest
from django.utils import timezone
from django.utils.crypto import get_random_string

from django_secret_sharing.utils import (
    URL_PART_ENCODING,
    create_secret,
    decrypt_value,
    encrypt_value,
    get_date_by_expires_value,
    get_secret_by_url_part,
)

ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24
ONE_WEEK = 60 * 60 * 24 * 7


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


def test_encrypt_and_decrypt():
    text = "Hellö, World!"
    key = get_random_string(32)
    iv = get_random_string(16)

    encrypted = encrypt_value(text, key=key, iv=iv)
    decrypted = decrypt_value(encrypted, key=key, iv=iv)

    assert decrypted == text.encode(URL_PART_ENCODING)


def test_get_date_by_expires_value():

    one_hour = get_date_by_expires_value(expires_value=ONE_HOUR)
    one_day = get_date_by_expires_value(expires_value=ONE_DAY)
    seven_days = get_date_by_expires_value(expires_value=ONE_WEEK)
    unused_value = get_date_by_expires_value(expires_value="1 year secret")

    assert (timezone.now() + timedelta(hours=1)).hour == one_hour.hour
    assert (timezone.now() + timedelta(days=1)).day == one_day.day
    assert (timezone.now() + timedelta(days=7)).day == seven_days.day
    assert not unused_value
