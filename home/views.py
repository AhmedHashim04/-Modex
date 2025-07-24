
from django.core.cache import cache
from django.views.generic import TemplateView
from product.models import Category, Product
from home.models import FeaturedProduct
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q,Count,Prefetch
from features.models import Tag
import random
from collections import defaultdict


def get_daily_products():
    products_data = cache.get('home_daily_products')

    if products_data is None:
        products = list(
            Product.objects.filter()
            # Product.objects.filter(is_available=True, trending=True)
            .values('id', 'name', 'slug', 'price', 'discount', 'trending', 'image', 'description', 'overall_rating')
        )

        product_ids = [p['id'] for p in products]

        tags_qs = Tag.objects.filter(products__id__in=product_ids).values('id', 'name', 'products__id')
        product_tags = defaultdict(list)

        for tag in tags_qs:
            product_tags[tag['products__id']].append({'id': tag['id'], 'name': tag['name']})

        for product in products:
            product['tags'] = product_tags[product['id']]

        cache.set('home_daily_products', products, 60 * 60)
        products_data = products
        print(len(products_data))

    daily_products = random.sample(products_data, k=min(6, len(products_data)))

    return daily_products

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        # Daily Products (random 100)
        # products_list = cache.get('home_daily_products')

        # if products_list is None:
        #     products_qs = Product.objects.filter(is_available=True, trending=True) \
        #         .only("id", "name", "slug", "price", "discount","image", "trending", "description", "overall_rating") \
        #         .prefetch_related(Prefetch("tags", queryset=Tag.objects.only("id", "name")))
        #     products_list = list(products_qs)
        #     cache.set('home_daily_products', products_list, 60 * 60)  # كاش لمدة ساعة

        # # كل ريكويست يختار 6 منتجات بشكل عشوائي من القائمة دي في الرام (بدون داتابيز)
        # daily_products = random.sample(products_list, k=min(len(products_list), 6))

        # # Sub Categories
        # sub_categories = cache.get('home_sub_categories')
        # if sub_categories is None:
        #     sub_categories = Category.objects.filter(
        #         parent__isnull=False,
        #     ).only('name', 'slug','image',"description")[:50]
        #     cache.set('home_sub_categories', sub_categories, 60 * 60 * 12)


        # # Main Categories
        # main_categories = cache.get('home_main_categories')
        # if main_categories is None:
        #     main_categories = Category.objects.filter(
        #         parent__isnull=True
        #     ).only('name', 'slug', 'image', 'description').annotate(product_count=Count('products'))

        #     cache.set('home_main_categories', main_categories, 60 * 60 * 24)

        # # # Trendy Products
        # trendy_products = cache.get('home_trendy_products')
        # if trendy_products is None:
        #     trendy_products = list(
        #         Product.objects.filter(
        #             is_available=True,
        #             trending=True
        #         )
        #         .only(
        #             "id", "name", "slug", "price", "discount", "description", "image", "overall_rating"
        #         )
        #         .prefetch_related(
        #             Prefetch("tags", queryset=Tag.objects.only("id", "name"))
        #         )[:20]
        #     )
        #     cache.set('home_trendy_products', trendy_products, 60 * 60 * 24)

        # # New Products
        # new_products = cache.get('home_new_products')
        # if new_products is None:
        #     new_products = Product.objects.filter(
        #         is_available=True,
        #         created_at__gte=timezone.now() - timezone.timedelta(days=30)
        #     ).only(
        #         "id", "name", "slug", "price", "discount", "image", "created_at", "category_id"
        #     ).select_related('category').order_by('-created_at')[:20]
        #     cache.set('home_new_products', new_products, 60 * 60 * 2)

        # # Top Rated
        # top_rated = cache.get('home_top_rated')
        # if top_rated is None:
        #     top_rated = Product.objects.filter(
        #         is_available=True,
        #         overall_rating__gte=4
        #     ).only(
        #         "id", "name", "slug", "price", "discount", "image", "overall_rating"
        #     ).order_by('-overall_rating')[:20]
        #     cache.set('home_top_rated', top_rated, 60 * 60 * 2)

        # # Discounts
        # discounts = cache.get('home_discounted_products')
        # if discounts is None:
        #     discounts = Product.objects.filter(
        #         is_available=True,
        #         discount__gte=15
        #     ).only(
        #         "id", "name", "slug", "price", "discount", "image"
        #     ).order_by('-discount')[:20]
        #     cache.set('home_discounted_products', discounts, 60 * 60 * 2)

        context.update({
            # 'main_categories': main_categories,
            # 'trendy_products_section': {
            #     'title': _("Trendy Products"),
            #     'products': trendy_products,
            #     'layout': 'carousel'
            # },
            'daily_products_section': {
                'title': _("Daily Products"),
                'products': get_daily_products(),
                # 'products': daily_products,
                'layout': 'grid'
            },
            # 'sub_categories_section': {
            #     'title': _("Sub Categories"),
            #     'products': sub_categories,
            #     'layout': 'carousel'
            # },
            # 'new_products_section': {
            #     'title': _("New Arrivals"),
            #     'products': new_products,
            #     'layout': 'grid'
            # },
            # 'top_rated_section': {
            #     'title': _("Top Rated"),
            #     'products': top_rated,
            #     'layout': 'grid'
            # },
            # 'discounts_section': {
            #     'title': _("Hot Deals"),
            #     'products': discounts,
            #     'layout': 'carousel'
            # }
        })

        return context


class RateLimitExceeded(HttpResponse):
    """
    HTTP 429 Too Many Requests response.
    Supports JSON and HTML responses, custom messages, and Retry-After header.
    """

    default_message = _("Rate limit exceeded. Please try again later.")

    def __init__(self, message=None, retry_after=None, as_json=False, extra_data=None, *args, **kwargs):
        message = message or self.default_message
        if as_json:
            data = {"detail": str(message)}
            if extra_data:
                data.update(extra_data)
            content_type = "application/json"
            content = JsonResponse(data, status=429)
            super().__init__(content=content.content, status=429, content_type=content_type, *args, **kwargs)
        else:
            super().__init__(str(message), status=429, *args, **kwargs)
        if retry_after is not None:
            # Accepts seconds or datetime
            if isinstance(retry_after, (int, float)):
                self["Retry-After"] = str(int(retry_after))
            elif isinstance(retry_after, timezone.datetime):
                self["Retry-After"] = retry_after.strftime("%a, %d %b %Y %H:%M:%S GMT")
