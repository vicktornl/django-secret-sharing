from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRET_SHARING_%s" % name, default)


EXPIRY_TIME_CHOICES = [
    (None, _("Select expiry time")),
    ((60 * 60), _("1 hour")),
    ((60 * 60 * 24), _("1 day")),
    ((60 * 60 * 24 * 7), _("1 week")),
]


EXPIRY_TIME_CHOICES = get_setting("EXPIRY_TIME_CHOICES", default=EXPIRY_TIME_CHOICES)
PASSWORD_LENGTH = get_setting("PASSWORD_LENGTH", default=32)
