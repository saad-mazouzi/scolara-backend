# Generated by Django 5.1.2 on 2024-11-14 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0020_user_salary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='salary',
            new_name='monthly_salary',
        ),
        migrations.AddField(
            model_name='user',
            name='session_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]