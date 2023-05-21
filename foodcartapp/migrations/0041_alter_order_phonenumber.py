# Generated by Django 3.2.15 on 2023-05-20 20:44

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_rename_count_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region='RU', verbose_name='Телефон'),
        ),
    ]
