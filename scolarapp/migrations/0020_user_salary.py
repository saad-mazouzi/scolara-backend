# Generated by Django 5.1.2 on 2024-11-13 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0019_transaction_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]