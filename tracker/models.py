from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="habits",
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    place = models.CharField(
        max_length=250,
        verbose_name="Место",
        help_text="Укажите место выполнения привычки",
    )
    time = models.TimeField(
        verbose_name="Время", help_text="Укажите время начала выполнения привычки"
    )
    action = models.CharField(
        max_length=250, verbose_name="Действие", help_text="Укажите действие"
    )
    nice = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Приятная или нет",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанные привычки",
        help_text="Выберете другие привычки, связанные с данной",
    )

    # Выбор периодичности привычки
    FREQUENCY_CHOICES = [
        ("once_a_week", "Раз в неделю"),
        ("twice_a_week", "Два раза в неделю"),
        ("three_a_week", "Три раза в неделю"),
        ("four_a_week", "Четыре раза в неделю"),
        ("five_a_week", "Пять раз в неделю"),
        ("six_a_week", "Шесть раз в неделю"),
        ("seven_a_week", "Каждый день"),
    ]
    periodicity = models.CharField(
        max_length=30,
        choices=FREQUENCY_CHOICES,
        default="once_a_week",
        verbose_name="Периодичность выполнения привычки",
        help_text="Укажите периодичность выполнения привычки",
    )
    # Вознаграждение
    reward = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение",
    )
    time_to_complete = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        blank=True,
        null=True,
        verbose_name="Время выполнения",
        help_text="Укажите время, необходимое для выполнения действия",
    )
    public = models.BooleanField(
        default=False,
        verbose_name="Публичная или нет",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
