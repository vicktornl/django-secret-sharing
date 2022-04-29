from email.policy import default

from django.conf import settings
from django.utils.translation import gettext as _


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRET_SHARING_%s" % name, default)


BACKEND = get_setting(
    "BACKEND", default=_("django_secret_sharing.backends.aws.AWSBackend")
)

#: backends
AWS_BUCKET = get_setting("AWS_BUCKET", default=_(""))
