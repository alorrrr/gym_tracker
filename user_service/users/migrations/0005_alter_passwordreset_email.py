# Generated by Django 5.1.6 on 2025-03-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
