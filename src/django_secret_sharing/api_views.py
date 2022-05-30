from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django_secret_sharing import serializers
from django_secret_sharing.exceptions import SecretNotFound
from django_secret_sharing.utils import create_secret, get_secret_by_url_part


@method_decorator(never_cache, name="dispatch")
@method_decorator(sensitive_post_parameters("value"), name="dispatch")
class SecretCreateView(APIView):
    def post(self, request):
        ser = serializers.SecretCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        secret, url_part = create_secret(
            value=ser.data.get("value"),
            expires_in=ser.data.get("expires"),
            view_once=ser.data.get("view_once"),
        )

        return Response({"url_part": url_part}, status=200)


@method_decorator(never_cache, name="dispatch")
@method_decorator(sensitive_post_parameters("url_part"), name="dispatch")
class SecretRetrieveView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = serializers.SecretRetrieveSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        url_part = ser.data.get("url_part")

        try:
            secret, value = get_secret_by_url_part(url_part)
        except SecretNotFound:
            raise Http404()

        if secret.view_once:
            secret.erase()

        return Response({"value": value})
