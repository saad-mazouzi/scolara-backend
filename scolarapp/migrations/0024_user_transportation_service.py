# Generated by Django 5.1.2 on 2024-11-18 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0023_user_monthly_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='transportation_service',
            field=models.BooleanField(default=False),
        ),
    ]
