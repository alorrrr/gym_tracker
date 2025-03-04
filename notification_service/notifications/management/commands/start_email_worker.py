from django.core.management.base import BaseCommand
from notifications.email_worker import start_email_worker

class Command(BaseCommand):
    help = 'Start the email worker to listen for messages from RabbitMQ'

    def handle(self, *args, **kwargs):
        start_email_worker()