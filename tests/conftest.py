from django.conf import settings


def pytest_configure():
    settings.configure(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite",}
        },
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.sitemaps",
            "django.contrib.staticfiles",
            "django_secret_sharing",
        ],
        MIDDLEWARE_CLASSES=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        ROOT_URLCONF="tests.urls",
        SECRET_KEY="tests",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                    "loaders": [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                },
            },
        ],
    )
