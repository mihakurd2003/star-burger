from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from django.utils import timezone
from requests.exceptions import HTTPError

from locationapp.models import Location
from foodcartapp.models import Order, Restaurant
from restaurateur.views import fetch_coordinates


@receiver(post_save, sender=Order)
def create_order_location(sender, instance, created, **kwargs):
    try:
        order_address_coord = fetch_coordinates(settings.GEO_API_KEY, instance.address)
    except HTTPError:
        return

    order_lon, order_lat = order_address_coord if order_address_coord else (None, None)

    if created:
        Location.objects.get_or_create(
            lat=order_lat,
            lon=order_lon,
            defaults={
                'address': instance.address,
            }
        )
    else:
        Location.objects.update_or_create(
            lat=order_lat,
            lon=order_lon,
            defaults={
                'address': instance.address,
            }
        )


@receiver(post_save, sender=Restaurant)
def create_restaurant_location(sender, instance, created, **kwargs):
    try:
        restaurant_address_coord = fetch_coordinates(settings.GEO_API_KEY, instance.address)
    except HTTPError:
        return

    restaurant_lon, restaurant_lat = restaurant_address_coord if restaurant_address_coord else (None, None)

    if created:
        Location.objects.get_or_create(
            lat=restaurant_lat,
            lon=restaurant_lon,
            defaults={
                'address': instance.address,
            }
        )
    else:
        Location.objects.update_or_create(
            address=instance.address,
            defaults={
                'lat': restaurant_lat,
                'lon': restaurant_lon,
                'request_dt': timezone.now(),
            }
        )
