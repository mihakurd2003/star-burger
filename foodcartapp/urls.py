from django.urls import path, include

from .views import product_list_api, register_order


app_name = "foodcartapp"

urlpatterns = [
    path('products/', product_list_api),
    path('banners/', include('banners.urls')),
    path('order/', register_order),
]
