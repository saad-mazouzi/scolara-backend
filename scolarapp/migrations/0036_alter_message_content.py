# Generated by Django 5.1.2 on 2024-12-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0035_chatroom_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]