from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum
from django.utils import timezone

from locationapp.models import Location


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                .filter(availability=True)
                .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=350,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):

    def get_order_price(self):
        order_items = self.annotate(order_cost=Sum(F('items__price') * F('items__quantity')))

        return order_items


class Order(models.Model):
    ORDER_STATUSES = [
        (0, 'Необработанный'),
        (1, 'Готовится'),
        (2, 'В доставке'),
        (3, 'Выполнен'),
    ]
    PAYMENT_METHODS = [
        ('cash', 'Наличностью'),
        ('electronic', 'Электронная'),
    ]

    firstname = models.CharField('Имя', max_length=50, db_index=True)
    lastname = models.CharField('Фамилия', max_length=50, db_index=True)
    phonenumber = PhoneNumberField('Телефон', db_index=True, region='RU')
    address = models.CharField('Адрес', max_length=200, db_index=True)
    status = models.IntegerField(
        'Статус заказа',
        choices=ORDER_STATUSES,
        default=0,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='В каком ресторане готовить',
        on_delete=models.CASCADE,
        related_name='orders',
        null=True, blank=True,
    )
    comment = models.TextField(
        'Комментарий',
        blank=True,
    )
    registrated_at = models.DateTimeField(
        'Дата и время оформления',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'Дата и время звонка',
        db_index=True,
        null=True, blank=True,
    )
    delivered_at = models.DateTimeField(
        'Дата и время доставки',
        db_index=True,
        null=True, blank=True,
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PAYMENT_METHODS,
        max_length=20,
        default='cash',
        db_index=True,
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.status = 1 if self.restaurant else 0
        super(Order, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='items',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items',
    )
    quantity = models.IntegerField('Количество', db_index=True)
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product} - {self.quantity}, {self.order}'



