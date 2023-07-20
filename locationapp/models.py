from django.db import models
from django.utils import timezone


class Location(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        unique=True,
    )
    lat = models.FloatField(
        'Широта',
        null=True,
    )
    lon = models.FloatField(
        'Долгота',
        null=True,
    )
    request_dt = models.DateTimeField(
        'Дата и время запроса',
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'местоположения'

    def __str__(self):
        return f'{self.address}'
