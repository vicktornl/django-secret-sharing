from django import forms
from django.utils.translation import ugettext_lazy as _


class CreateSecretForm(forms.Form):
    EXPIRY_CHOICES = [
        (3600, _("1 hour")),
        (3600, _("1 day")),
        (3600, _("1 week")),
    ]

    value = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": _("Secret content here")}),
    )
    expires_in = forms.ChoiceField(choices=EXPIRY_CHOICES)
