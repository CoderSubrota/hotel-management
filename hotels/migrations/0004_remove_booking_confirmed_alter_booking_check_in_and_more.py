# Generated by Django 5.1.6 on 2025-03-15 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_booking_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='confirmed',
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateTimeField(),
        ),
    ]
