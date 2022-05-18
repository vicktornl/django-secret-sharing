import pytest
from django.urls import reverse

from django_secret_sharing.models import Secret
from django_secret_sharing.utils import create_secret


@pytest.mark.django_db
def test_create_secret(client):
    res = client.post(
        reverse("django_secret_sharing:create"), data={"value": "My secret value"}
    )
    assert res.status_code == 200
    assert Secret.objects.get_non_erased().count() == 1


@pytest.mark.django_db
def test_retrieve_secret(client):
    secret, url_part = create_secret("My secret value")
    res = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )
    secret.refresh_from_db()
    assert res.status_code == 200
    assert not secret.erased


@pytest.mark.django_db
def test_retrieve_secret_not_found(client):
    res = client.get(
        reverse(
            "django_secret_sharing:retrieve",
            kwargs={"url_part": "icantfindthisurlpart"},
        )
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_retrieve_erased_secret_not_found(client):
    secret, url_part = create_secret("My secret value")
    secret.erase()
    res = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_view_secret(client):
    secret, url_part = create_secret("My secret value")
    res = client.get(
        reverse("django_secret_sharing:view", kwargs={"url_part": url_part})
    )
    secret.refresh_from_db()
    assert res.status_code == 200
    assert secret.erased


@pytest.mark.django_db
def test_view_secret_not_found(client):
    res = client.get(
        reverse(
            "django_secret_sharing:view",
            kwargs={"url_part": "icantfindthisurlpart"},
        )
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_view_erased_secret_not_found(client):
    secret, url_part = create_secret("My secret value")
    secret.erase()
    res = client.get(
        reverse("django_secret_sharing:view", kwargs={"url_part": url_part})
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_generate_password_view(client):
    res = client.get(
        reverse(
            "django_secret_sharing:generate-password",
        )
    )

    assert res.status_code == 200
    assert res.context["form"].initial["value"]
