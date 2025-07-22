
from django.core.cache import cache
from django.views.generic import TemplateView
from product.models import Category, Product
from home.models import FeaturedProduct
from django.utils.translation import gettext as _
from django.shortcuts import  render
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cache.get('home_data')
        if data is None:
            data = {

                'main_categories': Category.objects.filter(parent__isnull=True, products__isnull=False).distinct(),
                
                'featured_products_section': {
                    'title': _("Featured Products"), 
                    'products': FeaturedProduct.objects.filter(is_active=True).select_related('product').order_by('order')[:30],
                    'layout': 'carousel'  #'grid'
                },
                'daily_products_section': {
                    'title': _("Daily Products"),
                    'products': Product.objects.filter(is_available=True).order_by('?').select_related('category')[:100],
                    'layout': 'grid'
                },
                
                'sub_categories_section': {
                    'title': _("Sub Categories"), 
                    'products': Category.objects.filter(parent__isnull=False, products__isnull=False).distinct()[:50],
                    'layout': 'carousel'  # 'grid'
                },
                'new_products_section': {
                    'title': _("New Arrivals"),
                    'products': Product.objects.filter(is_available=True).order_by('-created_at').select_related('category')[:20],
                    'layout': 'grid'
                },
                'top_rated_section': {
                    'title': _("Top Rated"),
                    'products': Product.objects.filter(is_available=True, overall_rating__gte=4).order_by('-overall_rating')[:20],
                    'layout': 'grid'
                },
                

                'discounts_section': {
                    'title': _("Hot Deals"),
                    'products': Product.objects.filter(is_available=True, discount__gte=15).order_by('-discount')[:20],
                    'layout': 'carousel'
                },
            
            }
            cache.set('home_data', data, 60 * 60 * 24)  # 1 day
            
        context['data'] = data
        return context['data']
    


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
