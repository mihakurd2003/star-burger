from django.urls import path

from .views import get_banner, banners_list_api


app_name = "banners"

urlpatterns = [
    path('', banners_list_api),
    path('<slug:banner_slug>', get_banner),
]
