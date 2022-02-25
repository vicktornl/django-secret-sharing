import uuid

import pytest
from django.conf import settings
from django.core import signing
from django.utils.crypto import get_random_string

from django_secret_sharing.models import Secret
from django_secret_sharing.utils import (
    build_url,
    create_secret,
    decrypt_value,
    encrypt_value,
    parse_url_part,
)


@pytest.mark.django_db
def test_create_secret():
    value = "My secret value"
    secret, url = create_secret(value)
    assert secret
    assert secret.value != value
    assert url


def test_encrypt_and_decrypt():
    text = "Hellö, World!"
    key = get_random_string(32)
    iv = get_random_string(16)

    encrypted = encrypt_value(text, key=key, iv=iv)

    decrypted = decrypt_value(encrypted, key=key, iv=iv)

    assert decrypted == text.encode("utf-8")


def test_build_url_and_parse_url_part():
    key = get_random_string(32)
    iv = get_random_string(16)

    signed_id = signing.dumps(str(uuid.uuid4()), key=key)

    url_part = build_url(signed_id, key, iv)

    parsed_signed_id, parsed_key, parsed_iv = parse_url_part(url_part)

    assert parsed_signed_id == str(signed_id)
    assert parsed_key == key
    assert parsed_iv == iv
