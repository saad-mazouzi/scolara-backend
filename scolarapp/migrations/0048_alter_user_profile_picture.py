# Generated by Django 5.1.2 on 2024-12-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0047_timeslot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://scolara-bucket.s3.amazonaws.com/profile_pictures/profile_picture.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
