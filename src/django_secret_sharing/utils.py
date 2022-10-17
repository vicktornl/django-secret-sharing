import os
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.core import signing
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.module_loading import import_string

from django_secret_sharing import settings
from django_secret_sharing.exceptions import SecretNotFound
from django_secret_sharing.models import File, Secret
from django_secret_sharing.settings import BACKEND

ENCODING = "utf-8"
KEY_LENGTH = 32
IV_LENGTH = 16


def get_backend():
    backend = import_string(BACKEND)
    return backend()


def get_cipher(key: bytes, iv: bytes):
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
    )
    return cipher


def get_key_iv_pair() -> Tuple[bytes, bytes]:
    key = get_random_string(KEY_LENGTH).encode(ENCODING)
    iv = get_random_string(IV_LENGTH).encode(ENCODING)
    return key, iv


def transform_value_to_valid_block_length(
    value: bytes, block_length=16
) -> Tuple[bytes, int]:
    value_length = len(value)
    length_with_padding = value_length + (block_length - value_length) % block_length
    return value.ljust(length_with_padding, b"\0"), value_length


def encrypt_value(value: str, key: bytes, iv: bytes) -> Tuple[bytes, int]:
    bytes_value, bytes_value_length = transform_value_to_valid_block_length(
        value.encode(ENCODING)
    )
    cipher = get_cipher(key, iv)
    encryptor = cipher.encryptor()
    return (encryptor.update(bytes_value) + encryptor.finalize()), bytes_value_length


def decrypt_value(value: bytes, value_length: int, key: bytes, iv: bytes) -> str:
    cipher = get_cipher(key, iv)
    decryptor = cipher.decryptor()
    return (decryptor.update(value) + decryptor.finalize()).decode(ENCODING)[
        :value_length
    ]


def build_url_part(signed_id: str, value_length: int, key: str, iv: str) -> bytes:
    return urlsafe_base64_encode(
        f"{signed_id}{key}{iv}:{value_length}".encode(ENCODING)
    )


def create_files(file_refs: List[str]) -> List[File]:
    files = []
    return files


def create_secret(
    value: str,
    expires_in: Optional[int] = None,
    view_once: Optional[bool] = True,
    file_refs: List[str] = [],
) -> Tuple[Secret, str]:
    key, iv = get_key_iv_pair()
    salt = key.decode(ENCODING)
    expiry_date = get_date_by_expires_value(expires_in)
    encrypted_value, value_length = encrypt_value(value, key, iv)
    secret = Secret.objects.create(
        value=encrypted_value, expires_at=expiry_date, view_once=view_once
    )
    for file_ref in file_refs:
        if file_ref == "":
            continue
        File.objects.create(secret=secret, expires_in=expires_in, ref=file_ref)
    signed_id = signing.dumps(str(secret.id), salt=salt)
    url_part = build_url_part(
        signed_id, value_length, key.decode(ENCODING), iv.decode(ENCODING)
    )
    return secret, url_part


def get_secret_by_url_part(url_part: str) -> Tuple[Secret, str]:
    try:
        decoded_url_part = urlsafe_base64_decode(url_part).decode(ENCODING)
    except UnicodeDecodeError:
        raise SecretNotFound()

    value_length = decoded_url_part.rsplit(":", 1)[1]
    decoded_url_part = decoded_url_part[: -len(":%s" % value_length)]
    signed_id_length = len(decoded_url_part) - (KEY_LENGTH + IV_LENGTH)
    signed_id = decoded_url_part[:signed_id_length]
    key = decoded_url_part[signed_id_length:-IV_LENGTH].encode(ENCODING)
    iv = decoded_url_part[-IV_LENGTH:].encode(ENCODING)
    salt = key.decode(ENCODING)
    secret_id = validate_signed_id(signed_id, salt=salt)

    try:
        secret = Secret.objects.get_non_erased().get(id=secret_id)
        if secret.has_expired():
            secret.erase()
            raise Secret.DoesNotExist()
    except Secret.DoesNotExist:
        raise SecretNotFound()

    decrypted_value = decrypt_value(
        force_bytes(secret.value), int(value_length), key, iv
    )
    return secret, decrypted_value


def validate_signed_id(signed_id, salt):
    try:
        return signing.loads(signed_id, salt=salt)
    except signing.BadSignature:
        return None


def get_date_by_expires_value(expires_value: int) -> Union[datetime, None]:
    try:
        return timezone.now() + timedelta(seconds=expires_value)
    except:
        return None
