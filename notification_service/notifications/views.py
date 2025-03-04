from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_activation_email

# Create your views here.
