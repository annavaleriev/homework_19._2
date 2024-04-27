import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('catalog/fixtures/categories.json', 'r', encoding='utf-8') as file:
            categories_data = json.load(file)
        return categories_data

    @staticmethod
    def json_read_products():
        with open('catalog/fixtures/products.json', 'r', encoding='utf-8') as file:
            products_data = json.load(file)
        return products_data

    def handle(self, *args, **options):

        Product.objects.all().delete()

        Category.objects.all().delete()

        category_for_create = []
        products_for_create = []

        for category_data in self.json_read_categories():
            category_for_create.append(
                Category(title=category_data['fields']['title'], description=category_data['fields']['description'],
                         id=category_data['pk'])
            )

        Category.objects.bulk_create(category_for_create)

        for products_data in self.json_read_products():
            products_data_fields = products_data['fields']
            products_for_create.append(
                Product(
                    id=products_data["pk"],
                    title=products_data_fields['title'],
                    description=products_data_fields['description'],
                    image=products_data_fields['image'],
                    category=Category.objects.get(pk=products_data_fields['category']),
                    price=products_data_fields['price'],
                    created_at=products_data_fields['created_at'],
                    updated_at=products_data_fields['updated_at']
                )
            )

            Product.objects.bulk_create(products_for_create)
