from django.db import models


nullable = {'null': True, 'blank': True}


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

    def __str__(self):
        return f'{self.name} {self.cost}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

