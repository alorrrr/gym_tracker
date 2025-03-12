from django.test import TestCase
from ..models import CustomUser, PasswordReset
from rest_framework.authtoken.models import Token
from django.utils import timezone

class TestCustomUser(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create(username='test', password='Jojojo123')

        self.assertIsInstance(user, CustomUser)
        self.assertFalse(user.is_active)

class TestAuthTokenCreation(TestCase):
    def test_auth_token_creation(self):
        user = CustomUser.objects.create(username='test', password='Jojojo123')

        self.assertTrue(Token.objects.filter(user=user).exists())

class TestPasswordReset(TestCase):
    def setUp(self):
        self.password_reset = PasswordReset.objects.create(
            email = 'test@gmail.com',
            reset_code = '111111',
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
        )
    
    def test_expire_time(self):
        self.assertFalse(self.password_reset.is_expired())
        self.password_reset.expires_at = self.password_reset.created_at
        self.assertTrue(self.password_reset.is_expired())
