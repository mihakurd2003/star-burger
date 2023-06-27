from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import requests
from geopy import distance

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from foodcartapp.models import Product, Restaurant
from foodcartapp.models import Order
from locationapp.models import Location


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'invalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def find_common_objects(querysets):
    if not querysets:
        return None

    common_objects = querysets[0]
    for queryset in querysets:
        common_objects = common_objects.intersection(queryset)

    return common_objects


def get_distance(order):
    order_address_location = get_object_or_404(Location, address=order.address)
    if not order_address_location.lat:
        order.no_coordinates = True
        return

    order_lon, order_lat = order_address_location.lon, order_address_location.lat

    for restaurant in order.available_restaurants:
        restaurant_address_location = get_object_or_404(Location, address=restaurant.address)
        if not restaurant_address_location.lat:
            continue

        restaurant_lon, restaurant_lat = restaurant_address_location.lon, restaurant_address_location.lat
        restaurant.distance = f'- {round(distance.distance((order_lat, order_lon), (restaurant_lat, restaurant_lon)).km, 2)} км'


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = Order.objects.prefetch_related('items__product')\
        .get_order_price() \
        .order_by('status', 'id')

    for order in order_items:
        restaurants = [
            Restaurant.objects.filter(
                menu_items__product=item.product,
                menu_items__availability=True
            ) for item in order.items.all()
        ]
        order.available_restaurants = find_common_objects(restaurants)

        get_distance(order)

    return render(request, template_name='order_items.html', context={
        'order_items': order_items
    })
