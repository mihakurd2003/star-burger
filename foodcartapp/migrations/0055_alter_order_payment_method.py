# Generated by Django 4.2.1 on 2023-07-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_rename_registrated_at_order_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличностью'), ('electronic', 'Электронная')], db_index=True, max_length=20, verbose_name='Способ оплаты'),
        ),
    ]
