import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_create(api_client):
    url = reverse("users:register")
    data = {
        "email": "tamirmandreev@example.com",
        "password": "1234",
        "tg_chat_id": "1234",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(email=data["email"])
    assert user is not None
    assert user.password
    assert user.tg_chat_id == data["tg_chat_id"]
