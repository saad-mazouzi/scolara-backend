# Generated by Django 5.1.2 on 2024-11-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0028_teacheravailability'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='schools_logo/'),
        ),
    ]