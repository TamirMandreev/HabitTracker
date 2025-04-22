from django.urls import path

from tracker import views
from tracker.apps import TrackerConfig

app_name = TrackerConfig.name

urlpatterns = [
    path('habits/create/', views.HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/', views.HabitListAPIView.as_view(), name='habit-list'),
    path('habits/detail/<int:pk>/', views.HabitDetailAPIView.as_view(), name='habit-detail'),
    path('habits/update/<int:pk>/', views.HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/delete/<int:pk>/', views.HabitDeleteAPIView.as_view(), name='habit-delete'),
]