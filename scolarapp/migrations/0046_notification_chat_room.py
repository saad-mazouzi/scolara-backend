# Generated by Django 5.1.2 on 2024-12-13 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0045_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='chat_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.chatroom'),
        ),
    ]
