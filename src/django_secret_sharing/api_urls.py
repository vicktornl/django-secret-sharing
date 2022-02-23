from django.urls import path

from django_secret_sharing import api_views

app_name = "secrets"

urlpatterns = [
    path("", api_views.SecretCreateView.as_view(), name="create"),
    path("retrieve/", api_views.SecretRetrieveView.as_view(), name="retrieve"),
]
