from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .forms import OrderForm

from .models import Product
from .models import Order
from .serializers import OrderSerializer


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class OrderRegisterAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderUpdateAPIView(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class OrderDeleteAPIView(DestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'


# TODO: Внизу старый код, но полезный (1 способ)

@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = serializer.create(serializer.validated_data)
    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(['PUT'])
def update_order(request, id_order):
    if request.GET.get('in_admin', 0) and url_has_allowed_host_and_scheme(request.path, None):
        return redirect('admin:foodcartapp_order_change', id_order)

    order = get_object_or_404(Order, id=id_order)
    serializer = OrderSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    updated_order = serializer.update(order, serializer.validated_data)
    serializer = OrderSerializer(updated_order)

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_order(request, id_order):
    order = get_object_or_404(Order.objects.prefetch_related('items'), id=id_order)
    deleted_order = {
        'firstname': order.firstname,
        'lastname': order.lastname,
        'phonenumber': str(order.phonenumber),
        'address': order.address,
        'order_elements': [
            {
                'product': item.product.name,
                'quantity': item.quantity,
             } for item in order.items.all()
        ],
        'registered_at': order.registered_at,
        'called_at': order.called_at,
        'delivered_at': order.delivered_at,
    }
    order.delete()
    return Response(
        deleted_order,
        status=status.HTTP_200_OK,
    )


def edit_order(request, id_order):
    order = get_object_or_404(Order, id=id_order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

    else:
        form = OrderForm(instance=order)

    return render(request, 'edit_order.html', {'form': form})



