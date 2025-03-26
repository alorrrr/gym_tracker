from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserActivationView, CustomUserViewSet


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'auth', CustomUserViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]