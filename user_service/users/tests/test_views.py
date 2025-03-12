from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from ..models import CustomUser, PasswordReset
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from django.utils import timezone
import json


class TestUserViewSet(TestCase):
    def setUp(self):
        self.url = reverse('customuser-list')

    def test_creation_forbidden(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Creation is not allowed."})


class TestUserActivationView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password'
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('user-activate', args=[self.uid, self.token])
    
    def test_activation_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activation_user_not_found(self):
        invalid_url = reverse('user-activate', args=['nothing', 'invalid'])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activation_url_invalid(self):
        invalid_url = reverse('user-activate', args=[self.uid, 'invalid'])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCustomUserViewSet(TestCase):
    def setUp(self):
        self.registration_url = reverse('auth-list')
        self.password_reset_url = reverse('auth-reset-password')
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password'
        )
        self.user.is_active = True
        self.user.save()
        self.reset_code = '123456'
        self.password_reset = PasswordReset.objects.create(
            email=self.user.email,
            reset_code=self.reset_code,
            expires_at=timezone.now() + timezone.timedelta(minutes=10)
        )

    @patch('users.views.CustomUserViewSet.send_to_rabbitmq')
    def test_sending_activation_message(self, mock_send):
        user_data = {
            "username": "new_user",
            "password": "new_password",
            "email": "new@example.com"
        }
        response = self.client.post(self.registration_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mock_send.called)

        args = mock_send.call_args[0]
        message = json.loads(args[0])
        self.assertEqual(message['email'], "new@example.com")
        self.assertIn('activation_link', message)
    
    @patch('users.views.CustomUserViewSet.send_to_rabbitmq')
    def test_password_reset_code_sending(self, mock_send):
        user_data = {
            "email": "test@example.com"
        }
        response = self.client.post(self.password_reset_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(mock_send.called)

        args = mock_send.call_args[0]
        message = json.loads(args[0])
        self.assertEqual(message['email'], "test@example.com")
        self.assertIn('reset_code', message)

    @patch('users.views.CustomUserViewSet.send_to_rabbitmq')
    def test_password_reset_code_sending_user_not_found(self, mock_send):
        user_data = {
            "email": "nan@example.com"
        }
        response = self.client.post(self.password_reset_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(mock_send.called)

    def test_password_reset_success(self):
        url = reverse('auth-reset-password-confirm')
        reset_data = {
            'email': 'test@example.com',
            'new_password': 'new_password123',
            'reset_code': self.reset_code
        }
        response = self.client.post(url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))
    
    def test_password_reset_code_expired(self):
        url = reverse('auth-reset-password-confirm')

        self.password_reset.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        self.password_reset.save()
        reset_data = {
            'email': 'test@example.com',
            'new_password': 'new_password123',
            'reset_code': self.reset_code
        }
        response = self.client.post(url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Code expired'})

    def test_password_reset_user_not_found(self):
        url = reverse('auth-reset-password-confirm')
        reset_data = {
            'email': 'asd@example.com',
            'new_password': 'new_password123',
            'reset_code': self.reset_code
        }
        response = self.client.post(url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'User is not found'})
    
    def test_password_reset_code_invalid(self):
        url = reverse('auth-reset-password-confirm')
        reset_data = {
            'email': 'test@example.com',
            'new_password': 'new_password123',
            'reset_code': '123123'
        }
        response = self.client.post(url, reset_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Code is not right'})