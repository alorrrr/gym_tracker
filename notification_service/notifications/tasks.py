from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_email(email, activation_link):
    print('Sending')
    send_mail(
        subject='Activation on Gym Tracker!',
        message=f'Hello, to activate your account, go through the following link: {activation_link}',
        from_email='dibilarts@gmail.com',
        recipient_list=[email]
    )

@shared_task
def send_password_reset_email(email, reset_code):
    send_mail(
        subject='Password reset on Gym Tracker!',
        message=f'Your reset code: {reset_code}',
        from_email='dibilarts@gmail.com',
        recipient_list=[email],
    )