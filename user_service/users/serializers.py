import pika
import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from djoser.serializers import TokenCreateSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "id", "password", "is_active"]
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = 'CustomUserSerializer'