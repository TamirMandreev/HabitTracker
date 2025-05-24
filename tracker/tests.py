from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tracker.models import Habit
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_habit(api_client):
    """Тестирование создания новой привычки"""

    # Создать нового пользователя
    user = User.objects.create(email="tamirmandreev@mail.ru", password="1234")
    api_client.force_authenticate(user=user)

    # Создать данные для формирования POST-запроса
    data = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }
    # Отправить запрос
    response = api_client.post(
        reverse("tracker:habit-create"), data, format="json"
    )

    # Выполнить проверки
    assert response.status_code == status.HTTP_201_CREATED
    assert Habit.objects.count() == 1
    habit = Habit.objects.get(place="На улице")
    assert habit.place == data["place"]
    assert habit.time == datetime.strptime(data["time"], "%H:%M").time()
    assert habit.action == data["action"]
    assert habit.user == user


@pytest.mark.django_db
def test_list_habits(api_client):
    """Проверка отображения списка привычек текущего пользователя"""

    # Создать данные для формирования POST-запроса (для создания привычек)
    data1 = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }
    data2 = {"place": "Дома", "time": "18:30", "action": "Отжаться от пола"}

    # Создать 1 пользователя
    user1 = User.objects.create(
        email="user1@example.com", password="password1"
    )
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user1)
    # Создать 1 привычку
    api_client.post(reverse("tracker:habit-create"), data1, format="json")

    # Создать 2 пользователя
    user2 = User.objects.create(
        email="user2@example.com", password="password2"
    )
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user2)
    # Создать 2 привычку
    api_client.post(reverse("tracker:habit-create"), data2, format="json")

    # Отправить GET-запрос
    response = api_client.get(reverse("tracker:habit-list"), format="json")

    assert response.status_code == status.HTTP_200_OK

    assert (
        len(response.data["results"]) == 1
    )  # Убедиться, что видим только свою привычку


@pytest.mark.django_db
def test_list_public_habits(api_client):
    """Проверка публичного списка привычек"""
    # Создать данные для формирования POST-запроса (для создания привычек)
    data1 = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }
    data2 = {
        "place": "Дома",
        "time": "18:30",
        "action": "Отжаться от пола",
        "public": "True",
    }

    # Создать пользователя
    user = User.objects.create(email="user1@example.com", password="password1")
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user)
    # Создать привычки
    api_client.post(reverse("tracker:habit-create"), data1, format="json")
    api_client.post(reverse("tracker:habit-create"), data2, format="json")

    # Отправить GET-запрос на получение публичных привычек
    response = api_client.get(
        reverse("tracker:habit-list-public"), format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        len(response.data["results"]) == 1
    )  # Только одна публичная привычка должна быть видна


@pytest.mark.django_db
def test_update_habit(api_client):
    """Тестирование обновления привычки"""
    # Создать данные для формирования POST-запроса (для создания привычки)
    data = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }

    # Создать пользователя
    user = User.objects.create(email="user1@example.com", password="password1")
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user)
    # Создать привычку
    api_client.post(reverse("tracker:habit-create"), data, format="json")

    # Создать данные для обновления
    updated_data = {"place": "Дома"}

    # Отправить запрос на обновление
    response = api_client.patch(
        reverse("tracker:habit-update", kwargs={"pk": 6}),
        updated_data,
        format="json",
    )

    # Получить экземпляр модели Habit
    habit = Habit.objects.get(pk=6)

    assert response.status_code == status.HTTP_200_OK
    assert habit.place == updated_data["place"]


@pytest.mark.django_db
def test_delete_habit(api_client):
    """Тестирование удаления привычки"""
    # Создать данные для формирования POST-запроса (для создания привычки)
    data = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }

    # Создать пользователя
    user = User.objects.create(email="user1@example.com", password="password1")
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user)
    # Создать привычку
    api_client.post(reverse("tracker:habit-create"), data, format="json")

    # Отправить запрос на удаление
    response = api_client.delete(
        reverse("tracker:habit-delete", kwargs={"pk": 7}), format="json"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_detail_habit(api_client):
    """Тестирование обновления привычки"""
    # Создать данные для формирования POST-запроса (для создания привычки)
    data = {
        "place": "На улице",
        "time": "18:00",
        "action": "Подтянуться на турнике",
    }

    # Создать пользователя
    user = User.objects.create(email="user1@example.com", password="password1")
    # Аутентифицировать пользователя
    api_client.force_authenticate(user=user)
    # Создать привычку
    api_client.post(reverse("tracker:habit-create"), data, format="json")

    # Отправить запрос на получение объекта модели Habbit
    response = api_client.get(
        reverse("tracker:habit-detail", kwargs={"pk": 8}), format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["place"] == data["place"]
