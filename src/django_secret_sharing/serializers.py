from rest_framework import serializers

from django_secret_sharing.forms import CreateSecretForm


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)


class SecretUploadFileURLSerializer(serializers.Serializer):
    filename = serializers.CharField(required=True)
    expires_in = serializers.ChoiceField(
        choices=CreateSecretForm.EXPIRY_CHOICES, default=3600
    )
