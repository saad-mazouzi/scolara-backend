# Generated by Django 5.1.2 on 2025-01-21 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0002_location_remove_routestation_route_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetablesession',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.classroom'),
        ),
    ]
