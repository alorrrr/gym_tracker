import pika
import json
from random import choices
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.contrib.auth.tokens import default_token_generator
from djoser.views import UserViewSet as DjoserUserViewSet
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from .models import PasswordReset
from .serializers import UserSerializer



User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Creation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
    


class UserActivationView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": _("User activated successfully.")}, status=status.HTTP_200_OK)
        else:
            return Response({"error": _("Activation link is invalid.")}, status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [AllowAny] 
    def perform_create(self, serializer):
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            raise exceptions.ValidationError("User with this email already exists.")
        user = serializer.save()

        activation_link = self.generate_activation_link(user)
        message = json.dumps({
            'email': user.email,
            'activation_link': activation_link
        })
        self.send_to_rabbitmq(message)
    
    def generate_activation_link(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        return f"http://87.228.83.10/api/auth/activate/{uid}/{token}/"
    
    def send_to_rabbitmq(self, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials('myuser', 'Jojojo123')
            )
        )
        channel = connection.channel()
        print('Connection established')

        channel.queue_declare(queue='email_queue')
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)
        print('Message sent')

        connection.close()
    
    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.get_user()
        if user:
            reset_code = self.generate_reset_code()

            PasswordReset.objects.create(
                email=user.email,
                reset_code=reset_code,
                expires_at=timezone.now() + timedelta(minutes=10)
            )

            message = json.dumps({
                'email': user.email,
                'reset_code': reset_code,
            })

            self.send_to_rabbitmq(message)
        else:
            return Response({'error': 'User is not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def generate_reset_code(self):
        code = ''.join(choices("0123456789", k=6))
        return code

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        reset_code = request.data.get('reset_code')

        try:
            user = User.objects.filter(email=email).first()
            if user:
                reset_entry = PasswordReset.objects.get(email=email, reset_code=reset_code)
                if reset_entry.is_expired():
                    return Response({'error': 'Code expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                user.set_password(new_password)
                user.save()

                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({'error': 'User is not found'}, status=status.HTTP_404_NOT_FOUND)

        except PasswordReset.DoesNotExist:
            return Response({'error': 'Code is not right'}, status=status.HTTP_400_BAD_REQUEST)
