from django.urls import reverse
from django.views import generic

from django_secret_sharing.forms import CreateSecretForm
from django_secret_sharing.mixins import (
    RetrieveSecretMixin,
    SecretsMixin,
    ViewSecretMixin,
)


class CreateSecretView(SecretsMixin, generic.FormView):
    template_name = "django_secret_sharing/create.html"
    form_class = CreateSecretForm

    def get_success_url(self):
        return reverse("django_secret_sharing:create")

    def form_valid(self, form):
        secret = self.generate_url_part(form.cleaned_data)
        secret_url = self.get_secret_url(secret)
        context = self.get_context_data(secret_url=secret_url)
        return self.render_to_response(context)


class RetreiveSecretView(RetrieveSecretMixin, SecretsMixin, generic.TemplateView):
    template_name = "django_secret_sharing/retrieve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hash = kwargs["hash"]
        context.update(self.get_retrieve_context(hash))
        return context


class ViewSecretView(ViewSecretMixin, SecretsMixin, generic.TemplateView):
    template_name = "django_secret_sharing/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hash = kwargs["hash"]
        context.update(self.get_view_context(hash))
        return context
