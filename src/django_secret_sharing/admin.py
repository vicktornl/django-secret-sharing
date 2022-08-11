from django.contrib import admin

from django_secret_sharing import models


@admin.register(models.Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "expires_in",
        "erased",
        "view_once",
        "expires_at",
        "erased_at",
        "created_at",
    ]
    list_filter = [
        "erased",
        "view_once",
        "expires_at",
        "created_at",
        "erased_at",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.select_related("files")
        return qs


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "secret",
        "expires_in",
        "ref",
        "created_at",
    ]
    list_filter = [
        "created_at",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.select_related("secret")
        return qs
