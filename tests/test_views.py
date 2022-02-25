import pytest
from django.urls import reverse

from django_secret_sharing.models import Secret


@pytest.mark.django_db
def test_create_secret(client):
    res = client.post(
        reverse("django_secret_sharing:create"), data={"value": "My secret"}
    )
    assert res.status_code == 200
    assert Secret.objects.get_non_erased().count() == 1
