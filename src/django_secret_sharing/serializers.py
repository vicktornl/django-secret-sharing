from rest_framework import serializers


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)
