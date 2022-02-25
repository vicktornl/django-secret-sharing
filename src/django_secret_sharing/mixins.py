from django.core import signing
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes

from django_secret_sharing.exceptions import DecryptError
from django_secret_sharing.forms import CreateSecretForm
from django_secret_sharing.models import Secret
from django_secret_sharing.utils import (
    build_url,
    decrypt_value,
    encrypt_value,
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

        return build_url(signed_id, key, iv)

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
        try:
            signed_id, key, iv = parse_url_part(url_part)
        except UnicodeDecodeError:
            raise DecryptError()

        secret_id = validate_signed_id(signed_id, salt=key)
        try:
            return Secret.objects.get(id=secret_id)
        except Secret.DoesNotExist:
            return None

    def get_secret_url(self, secret):
        return self.request.build_absolute_uri(
            reverse("django_secret_sharing:retrieve", kwargs={"hash": secret})
        )


class ViewSecretMixin(SecretsMixin):
    def get_view_context(self, hash):
        context = {}
        try:
            context["secret"] = self.decrypt_secret(hash)
        except DecryptError:
            raise Http404()
        return context


class RetrieveSecretMixin(SecretsMixin):
    def get_retrieve_context(self, hash):
        context = {}
        if not self.validate_secret(hash):
            raise Http404()
        context["url_part"] = hash
        return context


class CreateSecretMixin(SecretsMixin):
    def get_create_context(self):
        return {"form": CreateSecretForm()}
