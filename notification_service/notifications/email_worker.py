import pika
import json
from .tasks import send_activation_email, send_password_reset_email

def start_email_worker():
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials('myuser', 'Jojojo123')
            )
        )
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    def callback(ch, method, properties, body):
        print("Received message:", body)
        data = json.loads(body)
        email = data['email']
        if 'activation_link' in data:
            activation_link = data['activation_link']
            send_activation_email.delay(email, activation_link)
        elif 'reset_code' in data:
            reset_code = data['reset_code']
            send_password_reset_email.delay(email, reset_code)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()