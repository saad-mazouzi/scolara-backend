# Generated by Django 5.1.2 on 2024-11-05 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0014_location_remove_transport_location_transportlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transports', to='scolarapp.school'),
            preserve_default=False,
        ),
    ]