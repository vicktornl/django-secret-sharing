from django import forms
from django.utils.translation import gettext_lazy as _

from django_secret_sharing import settings

EXPIRES_CHOICES = settings.EXPIRY_TIME_OPTIONS


class CreateSecretForm(forms.Form):
    expires = forms.ChoiceField(label=_("Expires in"), choices=EXPIRES_CHOICES)
    view_once = forms.BooleanField(
        label=_("View once"),
        widget=forms.CheckboxInput(attrs={"checked": "checked"}),
        required=False,
    )
    value = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": _("Secret content here")})
    )
