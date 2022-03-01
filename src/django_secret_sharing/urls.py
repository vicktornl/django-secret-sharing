from django.urls import path

from django_secret_sharing import views

app_name = "django_secret_sharing"


urlpatterns = [
    path("", views.CreateSecretView.as_view(), name="create"),
    path("<str:url_part>/", views.RetreiveSecretView.as_view(), name="retrieve"),
    path("<str:url_part>/view/", views.ViewSecretView.as_view(), name="view"),
]
