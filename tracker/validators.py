from rest_framework.exceptions import ValidationError


class ExcludeRelatedRewardValidator:
    """
    Исключает ситуацию, когда в экземпляре модели Habit
    одновременно присутствуют два поля: "related_habit" и "reward"
    """

    def __init__(self, object=None):
        # Указываем наименования полей
        self.related_habit_name = (
            "related_habit"  # Имя поля, которое обозначает связанную привычку
        )
        self.reward_name = "reward"  # Имя поля, которое обозначает награду

        self.object = object  # Экземпляр модели, в которую вносятся изменения

    def __call__(self, data):
        related_habit = data.get(
            self.related_habit_name
        )  # Получаем значение поля related_habit из переданных данных
        reward = data.get(
            self.reward_name
        )  # Получаем значение поля reward из переданных данных

        if related_habit and reward:
            raise ValidationError(
                f"Невозможно одновременно выбрать "
                f'"{self.related_habit_name}" и "{self.reward_name}". '
                f"Выберете только одно"
            )
        elif reward:
            if self.object:
                if self.object.related_habit:
                    raise ValidationError(
                        f"Невозможно одновременно выбрать "
                        f'"{self.related_habit_name}" и "{self.reward_name}". '
                        f"Выберете только одно"
                    )
        elif related_habit:
            if self.object.nice:
                raise ValidationError(
                    f"Невозможно одновременно выбрать "
                    f'"{self.related_habit_name}" и "{self.reward_name}". '
                    f"Выберете только одно"
                )


class LinkRelatedNiceValidator:
    """
    Исключает ситуацию, когда в объекте модели Habit
    при указании поля "related_habit", в объекте, с которым устанавливается
    связь ForeignKey, поле "nice" == False
    """

    def __init__(self):
        # Указываем наименования полей
        self.related_habit_name = (
            "related_habit"  # Имя поля, которое обозначает связанную привычку
        )
        self.nice_name = "nice"  # Имя поля, которое обозначает приятную привычку

    def __call__(self, data):
        related_habit = data.get(
            self.related_habit_name
        )  # Получаем значение поля related_habit из переданных данных. Это объект модели Habit.

        if related_habit:
            if related_habit.nice == False:
                raise ValidationError(
                    "В связанные привычки могут попадать "
                    "только привычки с признаком приятной привычки."
                    f"Если указано поле {self.related_habit_name}, "
                    f"поле {self.nice_name} объекта, с которым "
                    f"устанавливается связь ForeignKey должно быть True"
                )


class ExcludeNiceRewardOrRelatedValidator:
    """
    Исключает ситуацию, когда в объекте модели Habit
    поля nice==True и related_habit==True или reward==True
    """

    def __init__(self, object=None):
        self.object = object

    def __call__(self, data):
        if data.get("nice"):
            if data.get("related_habit") or data.get("reward"):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )
                if self.object:
                    if self.object.related_habit or self.object.reward:
                        raise ValidationError(
                            "У приятной привычки не может быть вознаграждения или связанной привычки."
                        )
        elif data.get("related_habit") or data.get("reward"):
            if self.object:
                if self.object.nice:
                    raise ValidationError(
                        "У приятной привычки не может быть вознаграждения или связанной привычки."
                    )
