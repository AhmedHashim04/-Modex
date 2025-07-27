
from django.core.cache import cache 
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from product.models import Category, Product,Tag
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q,Count,Prefetch
import random
from collections import defaultdict

CACHE_1_MINUTE = 60
CACHE_1_HOUR = CACHE_1_MINUTE * 60
CACHE_12_HOURS = CACHE_1_HOUR * 12
CACHE_6_HOURS = CACHE_1_HOUR * 6
CACHE_1_DAY = CACHE_1_HOUR * 24
CACHE_1_WEEK = CACHE_1_DAY * 7
CACHE_1_MONTH = CACHE_1_DAY * 30

CACHE_TIMES = {
    'daily_products': CACHE_1_DAY,
    'main_categories': CACHE_1_WEEK,
    'sub_categories': CACHE_1_WEEK,
    'trendy_products': CACHE_1_DAY,
    'new_products': CACHE_1_DAY,
    'top_rated': CACHE_1_DAY,
    'discounted_products': CACHE_1_DAY,
}

class HomeView(TemplateView):

    template_name = 'home/home.html'

    @staticmethod
    def get_all_available_products():
        return Product.objects.filter(is_available=True)

    @cached_property
    def cached_products(self):
        return self.get_all_available_products()

    def limited_product_query(self, queryset):
        return queryset.only(
            'id', 'name', 'slug', 'price', 'discount', 'image',
            'trending', 'overall_rating', 'description'
        ).prefetch_related('tags')

    def get_daily_products(self):
        products_data = cache.get('home:daily_products')
        if products_data is None:

            daily_products_qs = self.get_all_available_products().filter(trending=True)
            products = list(self.limited_product_query(daily_products_qs)[:100])
            cache.set('home:daily_products', products, CACHE_TIMES['daily_products'])
            products_data = products

        return random.sample(products_data, min(6, len(products_data)))

    def get_context_data(self, **kwargs):
        products_qs = self.cached_products

        context = super().get_context_data(**kwargs)

        # Sub Categories
        sub_categories = cache.get('home:sub_categories')
        if sub_categories is None:
            sub_categories = list(
                Category.objects.filter(parent__isnull=False)
                .values('name', 'slug', 'image')
            )
            cache.set('home:sub_categories', sub_categories, CACHE_TIMES['sub_categories'])

        # Main Categories
        main_categories = cache.get('home:main_categories')
        if main_categories is None:
            main_categories = list(
                Category.objects.filter(parent__isnull=True)
                .annotate(product_count=Count('products'))
                .values('name', 'slug', 'image', 'product_count','description')
            )
            cache.set('home:main_categories', main_categories, CACHE_TIMES['main_categories'])

        # Trendy Products
        trendy_products = cache.get('home:trendy_products')
        if trendy_products is None:
            trendy_products = list(self.limited_product_query(products_qs).filter(trending=True)[:15])
            cache.set('home:trendy_products', trendy_products, CACHE_TIMES['trendy_products'])

        # New Products
        new_products = cache.get('home:new_products')
        if new_products is None:
            new_products = list(self.limited_product_query(products_qs).order_by('-created_at')[:15])
            cache.set('home:new_products', new_products,  CACHE_TIMES['new_products'])

        # Top Rated
        top_rated = cache.get('home:top_rated')
        if top_rated is None:
            top_rated = list(
                self.limited_product_query(products_qs).filter(overall_rating__gte=4).order_by('-overall_rating')[:15]
            )
            cache.set('home:top_rated', top_rated, CACHE_TIMES['top_rated'])

        # Discounted Products
        discounts = cache.get('home:discounted_products')
        if discounts is None:
            discounts = list(
                self.limited_product_query(products_qs).filter(discount__gte=15).order_by('-discount')[:15]
            )
            cache.set('home:discounted_products', discounts, CACHE_TIMES['discounted_products'])

        context.update({
            'daily_products_section': {
                'title': _("Recommended Products"),
                'products': self.get_daily_products(),
                'layout': 'grid'
            },
            'main_categories': main_categories,
            'trendy_products_section': {
                'title': _("Trendy Products"),
                'products': trendy_products,
                'layout': 'carousel'
            },
            'sub_categories_section': {
                'title': _("Sub Categories"),
                'sub_categories': sub_categories,
                'layout': 'carousel'
            },
            'new_products_section': {
                'title': _("New Arrivals"),
                'products': new_products,
                'layout': 'grid'
            },
            'top_rated_section': {
                'title': _("Top Rated"),
                'products': top_rated,
                'layout': 'grid'
            },
            'discounts_section': {
                'title': _("Hot Deals"),
                'products': discounts,
                'layout': 'carousel'
            }
        })

        return context


class TermsOfServiceView(TemplateView):
    template_name = "static_pages/terms_of_service.html"
    
class PrivacyPolicy(TemplateView):
    template_name="static_pages/privacy_policy.html"



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

