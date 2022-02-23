import uuid

from django.conf import settings
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from vicktor.apps.secrets.utils import parse_url_part, validate_signed_id
from vicktor.models import MutationDateModel


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


class AbstractSecretsPage(RoutablePageMixin, Page):
    class Meta:
        abstract = True

    @route(r"^$")
    def default(self, *args, **kwargs):
        # TODO: render mixin view methods from django secret sharing
        raise Http404()

    @route(r"^(\w+)/$", name="url_part")
    def url_part(self, request, url_part=None, *args, **kwargs):
        # TODO: render mixin view methods from django secret sharing

        context = self.get_context(request, *args, **kwargs)

        try:
            signed_id, key, _iv = parse_url_part(url_part)
        except ValueError:
            raise Http404()

        secret_id = validate_signed_id(signed_id, salt=key)

        get_object_or_404(Secret.objects.get_non_erased(), id=uuid.UUID(secret_id))

        context.update(
            {"secret_url_part": url_part, "api_base_url": settings.API_BASE_URL}
        )

        return TemplateResponse(request, self.template, context)
