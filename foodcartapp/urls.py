from django.urls import path, include

from . import views


app_name = "foodcartapp"

urlpatterns = [
    path('products/', views.product_list_api),
    path('banners/', include('banners.urls')),
    path('order/', views.OrderRegisterAPIView.as_view()),
    path('order/<int:id>/edit', views.edit_order),
    path('order/<int:id>/update', views.OrderUpdateAPIView.as_view()),
    path('order/<int:id>/delete', views.OrderDeleteAPIView.as_view()),
]
