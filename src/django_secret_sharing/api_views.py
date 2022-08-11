import uuid

from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django_secret_sharing import serializers
from django_secret_sharing.exceptions import SecretNotFound
from django_secret_sharing.models import Secret
from django_secret_sharing.utils import (
    create_secret,
    get_backend,
    get_secret_by_url_part,
)


@method_decorator(never_cache, name="dispatch")
@method_decorator(sensitive_post_parameters("value"), name="dispatch")
class SecretCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = serializers.SecretCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        secret, url_part = create_secret(
            value=ser.data.get("value"),
            expires_in=ser.data.get("expires_in"),
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


@method_decorator(never_cache, name="dispatch")
class SecretUploadFileURLView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = serializers.SecretUploadFileURLSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        id = str(uuid.uuid4())
        filename = ser.data.get("filename")
        expires_in = ser.data.get("expires_in")
        backend = get_backend()
        url, fields = backend.get_upload_url(id, filename, expires_in=expires_in)

        return Response(
            {
                "filename": filename,
                "url": url,
                "fields": fields,
            }
        )
