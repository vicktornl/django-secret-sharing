from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

EXPIRES_CHOICES = (
    ("1 hour", _("1 hour")),
    ("1 day", _("1 day")),
    ("7 days", _("7 days")),
)


class SecretCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)
    one_time = serializers.BooleanField(required=False, default=True)
    expires = serializers.ChoiceField(choices=EXPIRES_CHOICES)


class SecretRetrieveSerializer(serializers.Serializer):
    url_part = serializers.CharField(required=True)
