from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import phonenumbers


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


def validate_fields(request_body, field_names):
    if not request_body:
        return Response({
            'response': 'no data',
        }, status=status.HTTP_400_BAD_REQUEST)

    for field_name in field_names:
        try:
            field = request_body[field_name]
        except KeyError:
            return Response({
                'error': f'{field_name} - обязательное поле.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if field_name != 'products' and isinstance(field, list):
            return Response({
                'error': f'В поле {field_name} положили список.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not field:
            return Response({
                'error': f'{field_name} поле не может быть пустым.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if field_name == 'products':
            if not isinstance(field, list):
                return Response({
                    'error': 'products: ожидался list со значениями, но был получен \'str\'.'
                }, status=status.HTTP_400_BAD_REQUEST)

            for product in field:
                if product['product'] > 200:
                    return Response({
                        'error': f'Недопустимый первичный ключ продукта \'{product["product"]}\''
                    }, status=status.HTTP_400_BAD_REQUEST)

        if field_name == 'phonenumber':
            error_msg = Response({
                'error': 'Введен некорректный номер телефона.'
            }, status=status.HTTP_400_BAD_REQUEST)
            try:
                phonenumber = phonenumbers.parse(field, 'RU')
                if not phonenumbers.is_valid_number(phonenumber):
                    return error_msg
            except phonenumbers.phonenumberutil.NumberParseException:
                return error_msg


@api_view(['POST'])
def register_order(request):
    requested_order = request.data

    not_valid = validate_fields(requested_order, field_names=['firstname', 'lastname', 'phonenumber', 'address', 'products'])
    if not_valid:
        return not_valid

    order, is_create = Order.objects.get_or_create(
        firstname=requested_order['firstname'],
        lastname=requested_order['lastname'],
        phonenumber=requested_order['phonenumber'],
        address=requested_order['address'],
    )

    products = requested_order['products']

    for product in products:
        order.items.get_or_create(
            product_id=product['product'],
            count=product['quantity'],
        )

    return Response(requested_order)
