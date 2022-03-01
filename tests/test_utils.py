import uuid

import pytest
from django.conf import settings
from django.core import signing
from django.utils.crypto import get_random_string

from django_secret_sharing.models import Secret
from django_secret_sharing.utils import (
    URL_PART_ENCODING,
    create_secret,
    decrypt_value,
    encrypt_value,
    get_secret_by_url_part,
)


@pytest.mark.django_db
def test_create_secret():
    raw_value = "My secret value"
    secret, url_part = create_secret(raw_value)
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
