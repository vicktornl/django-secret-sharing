import uuid

from django.conf import settings
from django.core import signing
from django.utils.crypto import get_random_string

from django_secret_sharing.utils import (
    decrypt_value,
    encrypt_value,
    get_url_part,
    parse_url_part,
)


def test_encrypt_and_decrypt():
    text = "Hellö, World!"
    key = get_random_string(32)
    iv = get_random_string(16)

    encrypted = encrypt_value(text, key=key, iv=iv)

    decrypted = decrypt_value(encrypted, key=key, iv=iv)

    assert decrypted == text.encode("utf-8")


def test_get_url_part_and_parse_url_part():
    key = get_random_string(32)
    iv = get_random_string(16)

    signed_id = signing.dumps(str(uuid.uuid4()), key=key)

    url_part = get_url_part(signed_id, key, iv)

    parsed_signed_id, parsed_key, parsed_iv = parse_url_part(url_part)

    assert parsed_signed_id == str(signed_id)
    assert parsed_key == key
    assert parsed_iv == iv
