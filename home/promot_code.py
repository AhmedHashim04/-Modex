import random
from collections import defaultdict
from django.core.cache import cache
from .models import Product, Tag  # عدّل المسار حسب مكان الموديلات

def get_daily_products(cache_key='home_daily_products', sample_size=6, cache_timeout=60 * 60):
    """
    ترجع عدد محدد من المنتجات اليومية (trending) من الكاش إن أمكن، وإلا بتجيبهم من الداتابيز.

    Args:
        cache_key (str): مفتاح الكاش.
        sample_size (int): عدد المنتجات اللي يتم اختيارهم عشوائيًا.
        cache_timeout (int): مدة بقاء الكاش بالثواني.

    Returns:
        list: قائمة المنتجات (كل منتج يحتوي على tags).
    """
    products_data = cache.get(cache_key)

    if products_data is None:
        products = list(
            Product.objects.filter(is_available=True, trending=True)
            .values('id', 'name', 'slug', 'price', 'discount', 'trending',
                    'image', 'description', 'overall_rating')
        )

        product_ids = [p['id'] for p in products]

        tags_qs = Tag.objects.filter(products__id__in=product_ids) \
            .values('id', 'name', 'products__id')

        product_tags = defaultdict(list)
        for tag in tags_qs:
            product_tags[tag['products__id']].append({'id': tag['id'], 'name': tag['name']})

        for product in products:
            product['tags'] = product_tags[product['id']]

        cache.set(cache_key, products, cache_timeout)
        products_data = products

    return random.sample(products_data, k=min(sample_size, len(products_data)))
