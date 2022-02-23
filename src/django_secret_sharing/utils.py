from Crypto.Cipher import AES
from django.conf import settings
from django.core import signing
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

URL_PART_ENCODING = "utf-8"


def encrypt_value(value, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(value)


def decrypt_value(value, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(value)


def get_url_part(signed_id, key, iv):
    return urlsafe_base64_encode(f"{signed_id}{key}{iv}".encode(URL_PART_ENCODING))


def parse_url_part(url_part):
    decoded_url_part = urlsafe_base64_decode(url_part).decode(URL_PART_ENCODING)

    signed_id_length = len(decoded_url_part) - (
        settings.SECRETS_AES_KEY_LENGTH + settings.SECRETS_AES_IV_LENGTH
    )
    iv_length = settings.SECRETS_AES_IV_LENGTH

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
