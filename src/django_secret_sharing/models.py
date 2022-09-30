import os
import uuid

from django.conf import settings
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class MutationDateModel(models.Model):
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, editable=False
    )
    modified_at = models.DateTimeField(_("modified at"), auto_now=True, editable=False)

    class Meta:
        abstract = True


class ExpiryModel(models.Model):
    expires_in = models.IntegerField(blank=False, null=True)

    class Meta:
        abstract = True


class SecretManager(models.Manager):
    def get_non_erased(self):
        return self.filter(erased=False)


class AbstractSecret(ExpiryModel, MutationDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.BinaryField(blank=True, null=True)
    erased = models.BooleanField(default=False)
    view_once = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    erased_at = models.DateTimeField(blank=True, null=True)

    objects = SecretManager()

    def erase(self, *args, **kwargs):
        self.value = None
        self.erased = True
        self.expires_at = None
        self.erased_at = timezone.now()
        self.save()

    def has_expired(self):
        if self.erased:
            return True
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    class Meta:
        abstract = True
        verbose_name = _("Secret")
        verbose_name_plural = _("Secrets")


class Secret(AbstractSecret):
    pass


class FileManager(models.Manager):
    pass


class AbstractFile(ExpiryModel, MutationDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret = models.ForeignKey(
        "django_secret_sharing.Secret",
        related_name="files",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    ref = models.TextField(unique=True)

    objects = FileManager()

    class Meta:
        abstract = True
        verbose_name = _("File")
        verbose_name_plural = _("Files")


class File(AbstractFile):
    @cached_property
    def filename(self):
        head, tail = os.path.split(self.ref)
        return tail

    @cached_property
    def download_url(self):
        from django_secret_sharing.utils import get_backend

        backend = get_backend()
        return backend.get_download_url(self)
