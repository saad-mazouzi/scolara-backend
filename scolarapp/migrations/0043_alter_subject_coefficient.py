# Generated by Django 5.1.2 on 2024-12-08 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0042_subject_coefficient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='coefficient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]