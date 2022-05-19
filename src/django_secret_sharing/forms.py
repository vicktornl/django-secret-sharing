from django import forms
from django.utils.translation import gettext_lazy as _

EXPIRES_CHOICES = (
    (None, _("Select expiry time")),
    ("1 hour", _("1 hour")),
    ("1 day", _("1 day")),
    ("7 days", _("7 days")),
)


class CreateSecretForm(forms.Form):
    expires = forms.ChoiceField(
        label=_("Expires in"), choices=EXPIRES_CHOICES, required=False
    )
    value = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": _("Secret content here")})
    )
