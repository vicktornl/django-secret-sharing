from django.core import signing
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes

from django_secret_sharing.exceptions import DecryptError
from django_secret_sharing.models import Secret
from django_secret_sharing.utils import (
    decrypt_value,
    encrypt_value,
    get_url_part,
    parse_url_part,
    validate_signed_id,
)


class SecretsMixin:
    """Mixin for generating url parts and decrypting secrets"""

    def generate_url_part(self, data):

        key = get_random_string(32)
        iv = get_random_string(16)

        encrypted_value = encrypt_value(data.get("value"), key=key, iv=iv)

        secret_instance = Secret.objects.create(value=encrypted_value)

        signed_id = signing.dumps(str(secret_instance.id), salt=key)

        return get_url_part(signed_id, key, iv)

    def decrypt_secret(self, url_part):
        try:
            signed_id, key, iv = parse_url_part(url_part)
        except UnicodeDecodeError:
            raise DecryptError()

        secret_id = validate_signed_id(signed_id, salt=key)
        secret = get_object_or_404(Secret.objects.get_non_erased(), id=secret_id)

        try:
            decrypted_value = decrypt_value(force_bytes(secret.value), key=key, iv=iv)
            decrypted_value_utf8 = decrypted_value.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            raise DecryptError()

        secret.erase()
        return decrypted_value_utf8

    def validate_secret(self, url_part):
        signed_id, key, iv = parse_url_part(url_part)

        secret_id = validate_signed_id(signed_id, salt=key)
        try:
            return Secret.objects.get(id=secret_id)
        except Secret.DoesNotExist:
            return None

    def get_secret_url(self, secret):
        return self.request.build_absolute_uri(
            reverse("django_secret_sharing:retrieve", kwargs={"hash": secret})
        )
