from django.test import TestCase
from ..models import Training, Exercise

class TestTraining(TestCase):
    def test_training_creation(self):
        training = Training.objects.create(
            user_id=1
        )
        self.assertTrue(isinstance(training, Training))

class TestExercise(TestCase):
    def setUp(self):
        self.training = Training.objects.create(user_id=1)
        
    def test_exercise_creation(self):
        exercise = Exercise.objects.create(
            name="Test Exercise",
            weight=50,
            reps=10,
            sets=5,
            training_id=self.training
        )
        self.assertTrue(isinstance(exercise, Exercise))