# Generated by Django 5.1.2 on 2024-12-08 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0041_remove_user_code_massar'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='coefficient',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
    ]
