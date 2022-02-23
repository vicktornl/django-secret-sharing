from django.contrib import admin

from django_secret_sharing import models


@admin.register(models.Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "erased",
        "erased_at",
        "created_at",
    ]
    list_filter = [
        "erased",
        "created_at",
        "erased_at",
    ]
