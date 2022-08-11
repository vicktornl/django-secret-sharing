from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from django_secret_sharing import settings
from django_secret_sharing.forms import CreateSecretForm


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    view_once = serializers.BooleanField(required=False, default=True)
    expires_in = serializers.ChoiceField(choices=settings.EXPIRY_TIME_CHOICES)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)


class SecretUploadFileURLSerializer(serializers.Serializer):
    filename = serializers.CharField(required=True)
    expires_in = serializers.ChoiceField(choices=settings.EXPIRY_TIME_CHOICES)
