from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
]