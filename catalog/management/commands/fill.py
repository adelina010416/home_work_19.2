from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Список категорий для добавления
        categories = [
            {'name': 'Овощи'},
            {'name': 'Фрукты'},
            {'name': 'Компьютеры'},
            {'name': 'Бытовая техника'}
        ]

        # Очистка таблицы Category
        Category.objects.all().delete()

        # Список экземпляров класса Category
        categories_for_create = []
        for category in categories:
            categories_for_create.append(Category(**category))

        # Добавление категорий в базу данных
        Category.objects.bulk_create(categories_for_create)

        # Список продуктов для добавления в БД
        products = [
            {'name': 'Огурец', 'cost': 5, 'category': categories_for_create[0]},  # Категория "овощи"
            {'name': 'Яблоко', 'cost': 5, 'category': categories_for_create[1]},  # Категория "фрукты"
            {'name': 'Ноутбук', 'cost': 5, 'category': categories_for_create[2]},  # Категория "компьютеры"
            {'name': 'Телевизор', 'cost': 5, 'category': categories_for_create[3]}  # Категория "бытовая техника"
        ]

        # Очистка таблицы Product
        Product.objects.all().delete()

        # Список экземпляров класса Product
        products_for_create = []
        for product in products:
            products_for_create.append(Product(**product))

        # Добавление продуктов в базу данных
        Product.objects.bulk_create(products_for_create)
