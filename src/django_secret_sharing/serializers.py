from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from django_secret_sharing import settings

EXPIRES_CHOICES = settings.EXPIRY_TIME_OPTIONS


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    view_once = serializers.BooleanField(required=False, default=True)
    expires = serializers.ChoiceField(choices=EXPIRES_CHOICES)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)
