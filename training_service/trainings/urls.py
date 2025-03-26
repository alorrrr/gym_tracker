from django.urls import path, include
from rest_framework import routers
from .views import TrainingViewSet, ExerciseViewSet

router = routers.SimpleRouter()
router.register(r"trainings", TrainingViewSet)
router.register(r"exercises", ExerciseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]