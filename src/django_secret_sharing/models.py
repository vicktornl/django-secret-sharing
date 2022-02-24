import uuid

from django.conf import settings
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MutationDateModel(models.Model):
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, editable=False
    )
    modified_at = models.DateTimeField(_("modified at"), auto_now=True, editable=False)

    class Meta:
        abstract = True


class SecretManager(models.Manager):
    def get_non_erased(self):
        return self.filter(erased=False)


class Secret(MutationDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.BinaryField(blank=True, null=True)
    erased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    erased_at = models.DateTimeField(blank=True, null=True)

    objects = SecretManager()

    def erase(self, *args, **kwargs):
        self.value = None
        self.erased = True
        self.erased_at = timezone.now()
        self.save()

    class Meta:
        verbose_name = _("Secret")
        verbose_name_plural = _("Secrets")
