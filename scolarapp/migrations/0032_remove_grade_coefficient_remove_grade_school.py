# Generated by Django 5.1.2 on 2024-11-26 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0031_control'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='coefficient',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='school',
        ),
    ]