from django.http import Http404
from django.urls import reverse
from django.views import generic

from django_secret_sharing.forms import CreateSecretForm
from django_secret_sharing.mixins import SecretsMixin


class CreateSecretView(generic.FormView, SecretsMixin):
    template_name = "secrets/index.html"
    form_class = CreateSecretForm

    def get_success_url(self):
        return reverse("django_secret_sharing:create")

    def form_valid(self, form):
        secret = self.generate_url_part(form.cleaned_data)
        secret_url = self.request.build_absolute_uri(
            reverse("django_secret_sharing:retrieve", kwargs={"hash": secret})
        )
        return self.render_to_response(self.get_context_data(secret_url=secret_url))


class RetreiveSecretView(generic.TemplateView, SecretsMixin):
    template_name = "secrets/retrieve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.validate_secret(kwargs["hash"]):
            raise Http404()
        context["url_part"] = kwargs["hash"]
        return context


class ViewSecretView(generic.TemplateView, SecretsMixin):
    template_name = "secrets/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["secret"] = self.decrypt_secret(kwargs["hash"])
        except:
            raise Http404()
        return context
