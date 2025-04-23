from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tracker.models import Habit
from tracker.validators import ExcludeRelatedRewardValidator, LinkRelatedNiceValidator, \
    ExcludeNiceRewardOrRelatedValidator


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [ExcludeRelatedRewardValidator(),
                      LinkRelatedNiceValidator(),]

    def validate(self, data):
        validator = ExcludeNiceRewardOrRelatedValidator(self.instance)
        validator(data)
        return data

