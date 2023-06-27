from django.db import models


class Banner(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=50,
        unique=True,
    )
    image = models.ImageField('Картинка')
    text = models.TextField(
        'Текст',
        max_length=150,
        null=True, blank=True,
    )
    slug = models.SlugField('Слаг', unique=True, blank=True)
    is_active = models.BooleanField('Активен', default=False)

    class Meta:
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'

    def __str__(self):
        return self.title
