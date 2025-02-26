from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserActivationView


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]