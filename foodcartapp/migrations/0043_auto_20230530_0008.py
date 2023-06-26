# Generated by Django 3.2.15 on 2023-05-29 21:08

from django.db import migrations
from django.db.models import F, Subquery, OuterRef


def fill_price_order_item(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    product = Subquery(OrderItem.objects.filter(id=OuterRef('id')).values('product__price'))
    OrderItem.objects.all().update(
        price=product * F('quantity')
    )


def rollback_price_order_item(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    OrderItem.objects.all().update(price=None)


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(fill_price_order_item, rollback_price_order_item)
    ]