# Generated by Django 5.1.2 on 2024-10-25 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetablesession',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.school'),
            preserve_default=False,
        ),
    ]
