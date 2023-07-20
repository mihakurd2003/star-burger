from phonenumber_field.serializerfields import PhoneNumberField
from django.db import transaction
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)
    phonenumber = PhoneNumberField()

    class Meta:
        model = Order
        fields = [
            'firstname', 'lastname',
            'phonenumber', 'address',
            'products', 'comment',
        ]

    @transaction.atomic
    def create(self, validated_data):
        order, is_create = Order.objects.get_or_create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address'],
        )

        product_fields = [{**field, 'price': field['product'].price} for field in validated_data['products']]
        products = [OrderItem(order=order, **product) for product in product_fields]
        OrderItem.objects.bulk_create(products)

        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.phonenumber = validated_data.get('phonenumber', instance.phonenumber)
        instance.address = validated_data.get('address', instance.address)
        instance.called_at = validated_data.get('called_at', instance.called_at)
        instance.delivered_at = validated_data.get('delivered_at', instance.delivered_at)
        instance.comment = validated_data.get('comment', instance.comment)

        if validated_data.get('products'):
            instance.items.all().delete()
            product_fields = [{**field, 'price': field['product'].price} for field in validated_data.get('products')]
            products = [OrderItem(order=instance, **product) for product in product_fields]
            OrderItem.objects.bulk_create(products)

        instance.save()
        return instance

