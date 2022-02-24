from django.utils.decorators import method_decorator
from django.views.decorators.debug import (
    sensitive_post_parameters,
    sensitive_variables,
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django_secret_sharing import serializers
from django_secret_sharing.mixins import SecretsMixin
from django_secret_sharing.models import Secret


@method_decorator(sensitive_variables(), name="dispatch")
@method_decorator(sensitive_post_parameters(), name="dispatch")
class SecretCreateView(SecretsMixin, APIView):
    def post(self, request):
        ser = serializers.SecretCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        url_part = self.generate_url_part(ser.data)
        return Response({"url_part": url_part}, status=200)


@method_decorator(sensitive_variables(), name="dispatch")
@method_decorator(sensitive_post_parameters(), name="dispatch")
class SecretRetrieveView(SecretsMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = serializers.SecretRetrieveSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        url_part = ser.data.get("url_part")
        decrypted_value = self.decrypt_secret(url_part)
        return Response({"value": decrypted_value})
