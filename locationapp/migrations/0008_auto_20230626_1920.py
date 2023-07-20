from django.db import migrations
from restaurateur.coordinates import fetch_coordinates

from django.conf import settings


def fill_locations(apps, schema_editor):
    Location = apps.get_model('locationapp', 'Location')
    Restaurant = apps.get_model('foodcartapp', 'Restaurant')
    Order = apps.get_model('foodcartapp', 'Order')
    orders, restaurants = Order.objects.all(), Restaurant.objects.all()

    for order in orders:
        order_address_coord = fetch_coordinates(settings.GEO_API_KEY, order.address)

        order_lon, order_lat = order_address_coord if order_address_coord else (None, None)

        Location.objects.get_or_create(
            address=order.address,
            defaults={
                'lat': order_lat,
                'lon': order_lon,
            }
        )

    for restaurant in restaurants:
        restaurant_address_coord = fetch_coordinates(settings.GEO_API_KEY, restaurant.address)

        restaurant_lon, restaurant_lat = restaurant_address_coord if restaurant_address_coord else (None, None)

        Location.objects.get_or_create(
            address=restaurant.address,
            defaults={
                'lat': restaurant_lat,
                'lon': restaurant_lon,
            }
        )


def rollback_locations(apps, schema_editor):
    Location = apps.get_model('locationapp', 'Location')
    Location.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('locationapp', '0007_alter_location_address'),
    ]

    operations = [
        migrations.RunPython(fill_locations, rollback_locations)
    ]
