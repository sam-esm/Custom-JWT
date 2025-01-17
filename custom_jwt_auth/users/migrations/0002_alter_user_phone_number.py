# Generated by Django 4.2.13 on 2024-06-03 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Wrong phone number format!', regex='^0\\d{10}$|^9\\d{9}$')]),
        ),
    ]
