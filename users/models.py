from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Почта',
        help_text='Укажите почту'
    )
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Телеграм chat_id',
        help_text='Укажите телеграм chat_id'
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',