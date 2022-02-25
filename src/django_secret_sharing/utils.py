from typing import Tuple

from Crypto.Cipher import AES
from django.core import signing
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django_secret_sharing.models import Secret

URL_PART_ENCODING = "utf-8"


def encrypt_value(value, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(value)


def decrypt_value(value, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(value)


def build_url(signed_id, key, iv):
    return urlsafe_base64_encode(f"{signed_id}{key}{iv}".encode(URL_PART_ENCODING))


def create_secret(value: str) -> Tuple[Secret, str]:
    key = get_random_string(32)
    iv = get_random_string(16)
    encrypted_value = encrypt_value(value, key=key, iv=iv)
    secret = Secret.objects.create(value=encrypted_value)
    signed_id = signing.dumps(str(secret.id), salt=key)
    url = build_url(signed_id, key, iv)
    return secret, url


def parse_url_part(url_part):
    decoded_url_part = urlsafe_base64_decode(url_part).decode(URL_PART_ENCODING)

    iv_length = 16
    signed_id_length = len(decoded_url_part) - (32 + iv_length)

    signed_id = decoded_url_part[:signed_id_length]
    key = decoded_url_part[signed_id_length:-iv_length]
    iv = decoded_url_part[-iv_length:]

    return (signed_id, key, iv)


def validate_signed_id(signed_id, salt):
    try:
        return signing.loads(signed_id, salt=salt)
    except signing.BadSignature:
        return None


def choice_to_datetime(choice):
    if choice == "1 hour":
        return timezone.now() + timezone.timedelta(hours=1)
    elif choice == "1 day":
        return timezone.now() + timezone.timedelta(days=1)
    else:
        return timezone.now() + timezone.timedelta(weeks=1)
