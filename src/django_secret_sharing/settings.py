from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRET_SHARING_%s" % name, default)


EXPIRY_TIME_CHOICES = [
    ((60 * 60), _("1 hour")),
    ((60 * 60 * 24), _("1 day")),
    ((60 * 60 * 24 * 7), _("1 week")),
]


EXPIRY_TIME_CHOICES = get_setting("EXPIRY_TIME_CHOICES", default=EXPIRY_TIME_CHOICES)
PASSWORD_LENGTH = get_setting("PASSWORD_LENGTH", default=32)
BACKEND = get_setting(
    "BACKEND", default="django_secret_sharing.backends.aws.AWSBackend"
)
AWS_BUCKET = get_setting("AWS_BUCKET", default="")
AWS_REGION = get_setting("AWS_REGION", default=None)
AWS_ENDPOINT_URL = get_setting("AWS_ENDPOINT_URL", default=None)
AWS_USE_SSL = get_setting("USE_SSL", default=None)
AWS_VERIFY = get_setting("VERIFY", default=None)
AWS_ACCESS_KEY_ID = get_setting("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = get_setting("AWS_SECRET_ACCESS_KEY", default=None)
AWS_SIGNATURE_VERSION = get_setting("AWS_SIGNATURE_VERSION", default=None)
