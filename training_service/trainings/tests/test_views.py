from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Training, Exercise


class TestTrainingViewSet(TestCase):
    def setUp(self):
        self.url = reverse('training-list')
        self.training = Training.objects.create(
            user_id=1,
            duration=10
        )
    
    def test_get_trainings(self):
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trainings_by_user_id(self):
        response = self.client.get(self.url, {'user_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_training(self):
        data = {
            "user_id": 1,
            "duration": 15
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), 2)

    def test_create_training_user_not_found(self):
        data = {
            "user_id": 999,
            "duration": 15
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class TestExerciseViewSet(TestCase):
    def setUp(self):
        self.url = reverse('exercise-list')
        self.training = Training.objects.create(
            user_id=1,
            duration=10
        )
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            weight=50,
            reps=10,
            sets=5,
            training_id=self.training
        )

    def test_get_exercise(self):
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_exercise_by_training_id(self):
        response = self.client.get(self.url, {'training_id': self.training.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        