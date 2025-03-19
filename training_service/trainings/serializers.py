from rest_framework.serializers import Serializer
from trainings.models import Training, Exercise


class TrainingSerializer(Serializer):
    class Meta:
        model = Training
        fields = '__all__'


class ExerciseSerializer(Serializer):
    class Meta:
        model = Exercise
        fields = '__all__'