# Generated by Django 5.1.2 on 2024-11-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0024_user_transportation_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='parent_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]