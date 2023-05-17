import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Product
from .models import Order


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


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


@api_view(['POST'])
def register_order(request):
    requested_order = request.data
    if not requested_order:
        return Response({
            'response': 'no data',
        })

    order, is_create = Order.objects.get_or_create(
        firstname=requested_order['firstname'],
        lastname=requested_order['lastname'],
        phonenumber=requested_order['phonenumber'],
        address=requested_order['address'],
    )
    try:
        products = requested_order['products']
    except KeyError:
        return Response({
            'error': 'products - обязательное поле.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if products is None:
        return Response({
            'error': 'products поле не может быть пустым.'
        }, status=status.HTTP_400_BAD_REQUEST)

    elif not isinstance(products, list):
        return Response({
            'error': 'products: ожидался list со значениями, но был получен \'str\'.'
        }, status=status.HTTP_400_BAD_REQUEST)

    elif not products:
        return Response({
            'error': 'Список products не может быть пустым.'
        }, status=status.HTTP_400_BAD_REQUEST)

    for product in products:
        order.items.get_or_create(
            product_id=product['product'],
            count=product['quantity'],
        )

    return Response(requested_order)
