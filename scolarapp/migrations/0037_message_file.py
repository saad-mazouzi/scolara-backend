# Generated by Django 5.1.2 on 2024-12-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0036_alter_message_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='chat_files/'),
        ),
    ]
