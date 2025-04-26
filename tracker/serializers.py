from rest_framework.serializers import ModelSerializer

from tracker.models import Habit
from tracker.validators import (
    ExcludeNiceRewardOrRelatedValidator,
    ExcludeRelatedRewardValidator,
    LinkRelatedNiceValidator,
)


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            LinkRelatedNiceValidator(),
        ]

    def validate(self, data):
        first_validator = ExcludeNiceRewardOrRelatedValidator(self.instance)
        first_validator(data)

        second_validator = ExcludeRelatedRewardValidator(self.instance)
        second_validator(data)

        return data
