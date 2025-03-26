import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Training, Exercise
from .serializers import TrainingSerializer, ExerciseSerializer


class TrainingViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Error": str(e)})
            
    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('user_id'):
            return Training.objects.filter(user_id=self.request.query_params.get('user_id'))
        return Training.objects.all()

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')

        response = requests.get(f'http://user-service:8000/api/users/{user_id}/')

        if response.status_code == 200:
            if response.json().get('is_active'):
                serializer.save()
            else:
                raise Exception('User is not active')
        else:
            raise Exception('User not found')


class ExerciseViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('training_id'):
            return Exercise.objects.filter(training_id=self.request.query_params.get('training_id'))
        return Exercise.objects.all()