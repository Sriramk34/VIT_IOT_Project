# Generated by Django 4.1.2 on 2022-11-16 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='time',
            field=models.DateTimeField(blank=True),
        ),
    ]
