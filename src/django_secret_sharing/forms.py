from django import forms
from django.utils.translation import ugettext_lazy as _


class CreateSecretForm(forms.Form):
    value = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": _("Secret content here")})
    )
