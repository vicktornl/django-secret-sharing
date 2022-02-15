from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, "DJANGO_SECRETS_SHARING_%s" % name, default)
