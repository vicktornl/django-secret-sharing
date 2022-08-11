from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("django_secret_sharing.api_urls")),
    path("", include("django_secret_sharing.urls")),
]
