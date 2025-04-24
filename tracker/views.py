from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from tracker.models import Habit
from tracker.paginations import CustomPagination
from tracker.permissions import IsUser
from tracker.serializers import HabitSerializer


# Create your views here.

class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer

    # Добавить автоматическое заполнение поля user
    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = (IsUser,)


class HabitDetailAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)


class HabitDeleteAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)