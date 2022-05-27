from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRET_SHARING_%s" % name, default)


EXPIRY_TIME_OPTIONS = [
    (None, _("Select expirey time")),
    ((60 * 60), _("1 hour")),
    ((60 * 60 * 24), _("1 day")),
    ((60 * 60 * 24 * 7), _("7 days")),
]


EXPIRY_TIME_OPTIONS = get_setting("EXPIRY_TIME_OPTIONS", default=EXPIRY_TIME_OPTIONS)
PASSWORD_LENGTH = get_setting("PASSWORD_LENGTH", default=32)
