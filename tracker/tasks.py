from datetime import datetime, time

from celery import shared_task

from tracker.models import Habit
from tracker.services import send_telegram_message
from users.models import User


@shared_task
def reminder_of_habit():
    # Получить все привычки
    habits = Habit.objects.all()
    # Получить текущую дату и время
    current_time = datetime.now()
    # Преобразовать current_time в формат "20:00:00".
    # Дата убирается, остается только время.
    valid_current_time = time(
        hour=current_time.hour,
        minute=current_time.minute,
        second=current_time.second,
    )

    for habit in habits:
        if habit.time == valid_current_time:
            tg_chat_id = habit.user.tg_chat_id
            message = f"Пришло время {habit.action}"
            send_telegram_message(tg_chat_id, message)


@shared_task
def information_about_today():
    users = User.objects.all()
    for user in users:
        habits = user.habits.all()
        message = "Сегодня вам нужно выполнить: \n"
        for habit in habits:
            message += f"{habit.action} в {habit.time} в {habit.place}\n"
        send_telegram_message(user.tg_chat_id, message)
