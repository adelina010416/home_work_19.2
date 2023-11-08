from django.db import models

from constants import nullable
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(max_length=250, **nullable, verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(max_length=250, **nullable, verbose_name='описание')
    image = models.ImageField(upload_to='products/', **nullable, verbose_name='превью')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    cost = models.IntegerField(verbose_name='цена')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')  # дата создания
    last_change_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')  # дата последнего изменения
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **nullable, verbose_name='владелец')

    def __str__(self):
        return f'{self.name} {self.cost}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Version(models.Model):
    VERSION_CHOICES = ((True, 'активная'), (False, 'не активная'))

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.PositiveIntegerField(default=1, verbose_name='Номер версии')
    version_name = models.CharField(max_length=250, verbose_name='Название версии', **nullable)
    is_current = models.BooleanField(choices=VERSION_CHOICES, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.product} v. {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('version_number',)
