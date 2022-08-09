from django import forms
from django.utils.translation import gettext_lazy as _

from django_secret_sharing import settings


class CreateSecretForm(forms.Form):
    expires = forms.TypedChoiceField(
        label=_("Expires in"), choices=settings.EXPIRY_TIME_CHOICES, coerce=int
    )
    view_once = forms.BooleanField(
        label=_("View once"),
        help_text=_(
            "When checked the message will only be able to be viewed once and then disappears forever"
        ),
        widget=forms.CheckboxInput(attrs={"checked": "checked"}),
        required=False,
    )
    value = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": _("Secret content here")}),
    )
