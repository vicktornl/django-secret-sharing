from datetime import timedelta

import pytest
from django.urls import reverse

from django_secret_sharing.models import Secret
from django_secret_sharing.utils import create_secret

ONE_HOUR = 60 * 60


@pytest.mark.django_db
def test_create_secret(client):
    res = client.post(
        reverse("django_secret_sharing:create"),
        data={"value": "My secret value", "expires": ONE_HOUR, "view_once": True},
    )

    assert res.status_code == 200
    assert Secret.objects.get_non_erased().count() == 1
    assert Secret.objects.first().expires_at


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
def test_retrieve_secret_with_expiry_time(client):
    secret, url_part = create_secret("My secret value", expires_in=ONE_HOUR)
    res = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )
    secret.refresh_from_db()
    assert res.status_code == 200
    assert not secret.erased
    assert secret.expires_at


@pytest.mark.django_db
def test_retrieve_expired_secret(client):
    secret, url_part = create_secret("My secret value", expires_in=ONE_HOUR)
    secret.expires_at = secret.expires_at - timedelta(days=7)
    secret.save()
    res = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )

    secret.refresh_from_db()
    assert res.status_code == 404
    assert secret.erased
    assert not secret.expires_at


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


@pytest.mark.django_db
def test_view_secret_more_then_once(client):
    secret, url_part = create_secret(
        "My secret value", expires_in=ONE_HOUR, view_once=False
    )

    res = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )

    res2 = client.get(
        reverse("django_secret_sharing:retrieve", kwargs={"url_part": url_part})
    )

    assert res.status_code == 200
    assert res2.status_code == 200


@pytest.mark.django_db
def test_value_field_is_required(client):
    res = client.post(
        reverse("django_secret_sharing:create"),
        data={"value": "", "expires": ONE_HOUR, "view_once": True},
    )

    assert res.context_data["form"]._errors["value"]
    assert Secret.objects.count() == 0


@pytest.mark.django_db
def test_expires_field_is_required(client):
    res = client.post(
        reverse("django_secret_sharing:create"),
        data={"value": "My secret value", "expires": "", "view_once": True},
    )

    assert res.context_data["form"]._errors["expires"]
    assert Secret.objects.count() == 0


@pytest.mark.django_db
def test_expires_value_not_in_choices(client):
    res = client.post(
        reverse("django_secret_sharing:create"),
        data={"value": "My secret value", "expires": 9999999999, "view_once": True},
    )

    assert res.context_data["form"]._errors["expires"]
    assert Secret.objects.count() == 0


# TODO: Test ref cant be manipulated in order to download other files
