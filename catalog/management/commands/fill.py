import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('categories.json', 'r') as file:
            categories_data = json.load(file)
        return categories_data

    @staticmethod
    def json_read_products():
        with open('products.json', 'r') as file:
            products_data = json.load(file)
        return products_data

    def handle(self, *args, **options):

        Product.objects.all().delete()

        Category.objects.all().delete()

        category_for_create = []
        products_for_create = []

        for category_data in Command.json_read_categories():
            category_for_create.append(
                Category(title=category_data['title'], description=category_data['description'])
            )

        Category.objects.bulk_create(category_for_create)

        for products_data in Command.json_read_products():
            # products_for_create.append(
            #     Product(title=products_data['title'], description=products_data['description'],
            #             image=products_data['image'], category=products_data['category'],
            #             price=products_data['price'], created_at=products_data['created_at'],
            #             updated_at=products_data['updated_at']
            #             )
            # )
            product = Product(**products_data)
            products_for_create.append(product)

            Product.objects.bulk_create(products_for_create)

            # а с id что делать? Он же есть в базе

            # def handle(self, *args, **options):
            #     category_list = [
            #         {'title': "Продукты", 'description': "Замороженные"},
            #         {'title': "Корм", 'description': "Для животных"},
            #         {'title': "Бытовая химия", 'description': "Для дома"},
            #     ]
            #
            #     category_for_create = []
            #     for category_item in category_list:
            #         category_for_create.append(
            #             Category(**category_item)
            #         )
