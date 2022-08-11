from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_secret_sharing import settings
from django_secret_sharing.models import File
from django_secret_sharing.utils import get_backend


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
    file_refs = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    def clean_file_refs(self):
        file_refs = self.cleaned_data["file_refs"]
        file_refs = (
            self.cleaned_data["file_refs"].split(",") if file_refs is not "" else []
        )

        if File.objects.filter(ref__in=file_refs).exists():
            raise ValidationError(_("File(s) already exists"))

        backend = get_backend()

        if not backend.validate_file_refs(file_refs):
            raise ValidationError(_("File(s) not uploaded"))

        return file_refs
