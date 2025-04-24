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

    # Пользователь получает список только своих привычек
    def get_queryset(self):
        user = self.request.user
        queryset = Habit.objects.filter(user=user)
        return queryset


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


class HabitPublicListAPIView(ListAPIView):
    queryset = Habit.objects.filter(public=True)
    serializer_class = HabitSerializer
    pagination_class = CustomPagination