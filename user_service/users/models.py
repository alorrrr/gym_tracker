from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=False) 


class PasswordReset(models.Model):
    email = models.EmailField()
    reset_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=SocialAccount)
def activate_user_on_social_login(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user and not user.is_active:
            user.is_active = True
            user.save()