from django.http import Http404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from django_secret_sharing import settings
from django_secret_sharing.exceptions import SecretNotFound
from django_secret_sharing.forms import CreateSecretForm
from django_secret_sharing.utils import create_secret, get_secret_by_url_part


@method_decorator(never_cache, name="dispatch")
@method_decorator(sensitive_post_parameters("value"), name="dispatch")
class CreateSecretView(generic.FormView):
    template_name = "django_secret_sharing/create.html"
    form_class = CreateSecretForm

    def get_success_url(self):
        return reverse("django_secret_sharing:create")

    def form_valid(self, form):
        secret, url_part = create_secret(
            value=form.cleaned_data.get("value"),
            expires_in=form.cleaned_data.get("expires"),
            view_once=form.cleaned_data.get("view_once"),
        )

        context = super().get_context_data()
        context["secret"] = secret
        context["secret_url"] = self.request.build_absolute_uri(
            reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
        )
        return self.render_to_response(context)


@method_decorator(never_cache, name="dispatch")
class RetreiveSecretView(generic.TemplateView):
    template_name = "django_secret_sharing/retrieve.html"

    def get_context_data(self, **kwargs):
        url_part = kwargs["url_part"]

        try:
            secret, value = get_secret_by_url_part(url_part)
        except SecretNotFound:
            raise Http404()

        context = super().get_context_data(**kwargs)
        context["secret"] = secret
        context["url_part"] = url_part
        return context


@method_decorator(never_cache, name="dispatch")
class ViewSecretView(generic.TemplateView):
    template_name = "django_secret_sharing/view.html"

    def get_context_data(self, **kwargs):
        url_part = kwargs["url_part"]

        try:
            secret, value = get_secret_by_url_part(url_part)
        except SecretNotFound:
            raise Http404()

        if secret.view_once:
            secret.erase()

        context = super().get_context_data(**kwargs)
        context["secret"] = secret
        context["value"] = value
        return context


class GeneratePasswordView(CreateSecretView):
    def get_initial(self):
        initial = super().get_initial()
        initial["value"] = get_random_string(settings.PASSWORD_LENGTH)
        return initial
