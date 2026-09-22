from rest_framework import serializers

from django_secret_sharing import settings


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    view_once = serializers.BooleanField(required=False, default=True)
    expires_in = serializers.ChoiceField(choices=settings.EXPIRY_TIME_CHOICES)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)


class SecretUploadFileURLSerializer(serializers.Serializer):
    filename = serializers.CharField(required=True)
    expires_in = serializers.ChoiceField(choices=settings.EXPIRY_TIME_CHOICES)
