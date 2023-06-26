# Generated by Django 4.2.1 on 2023-06-20 19:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locationapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='request_dt',
            field=models.DateTimeField(default=django.utils.timezone.now, unique=True, verbose_name='Дата и время запроса'),
        ),
    ]
