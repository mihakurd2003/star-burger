# Generated by Django 4.2.1 on 2023-07-20 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='registrated_at',
            new_name='registered_at',
        ),
    ]
