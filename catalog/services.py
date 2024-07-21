from django.core.cache import cache

from catalog.models import Category, Product


def get_categories():
    """Возвращает список категорий"""
    cache_key = 'all_categories'
    categories = cache.get(cache_key)

    if not categories:
        Category.objects.all()
        cache.set(cache_key, categories)
    return categories


def get_products():
    """Возвращает список продуктов"""
    cache_key = 'all_products'
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.all()
        cache.set(cache_key, products)
    return products
