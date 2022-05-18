from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRET_SHARING_%s" % name, default)


PASSWORD_LENGTH = get_setting("PASSWORD_LENGTH", default=32)