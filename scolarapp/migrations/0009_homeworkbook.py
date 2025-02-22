# Generated by Django 5.1.2 on 2025-02-22 22:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0008_remove_user_next_payment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('homework_due_date', models.DateField(verbose_name='Homework Due Date')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_books', to='scolarapp.educationlevel', verbose_name='Education Level')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'TEACHER'}, on_delete=django.db.models.deletion.CASCADE, related_name='homework_books', to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'Homework Book',
                'verbose_name_plural': 'Homework Books',
                'ordering': ['-created_at'],
            },
        ),
    ]
