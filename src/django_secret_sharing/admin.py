from django.contrib import admin

from django_secret_sharing import models


@admin.register(models.Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = [
        "id",
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
