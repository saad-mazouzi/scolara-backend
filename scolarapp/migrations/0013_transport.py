# Generated by Django 5.1.2 on 2024-11-05 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0012_subject_education_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('registration', models.CharField(blank=True, max_length=20, null=True)),
                ('location', models.CharField(max_length=255)),
                ('driver', models.ForeignKey(limit_choices_to={'role__name': 'Chauffeur'}, on_delete=django.db.models.deletion.CASCADE, related_name='driven_transports', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(limit_choices_to={'role__name': 'Étudiant'}, on_delete=django.db.models.deletion.CASCADE, related_name='student_transports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]