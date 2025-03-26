from rest_framework.serializers import ModelSerializer
from trainings.models import Training, Exercise


class TrainingSerializer(ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'