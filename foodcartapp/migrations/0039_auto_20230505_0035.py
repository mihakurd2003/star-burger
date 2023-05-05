# Generated by Django 3.2.15 on 2023-05-04 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20230504_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='foodcartapp.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='foodcartapp.product', verbose_name='Товар'),
        ),
    ]
