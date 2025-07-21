
from django.core.cache import cache
from django.views.generic import TemplateView
from product.models import Category, Product
from home.models import FeaturedProduct
from django.utils.translation import gettext as _
from django.shortcuts import  render

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
                    'products': Product.objects.filter(is_available=True).order_by('?').select_related('category')[:20],
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
                

                # 'collections_section': {
                #     'title': _("Our Collections"),
                #     'collections': Collection.objects.filter(is_active=True).annotate(
                #         product_count=Count('products')
                #     ).filter(product_count__gt=0).order_by('-created_at')[:6],
                #     'layout': 'carousel'
                # },
                
                # # قسم المدونة أو المحتوى (إن وجد)
                # 'blog_section': {
                #     'title': _("Latest News"),
                #     'posts': BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3]
                # },
                
                # قسم العلامات التجارية (إن وجد)
                # 'brands_section': {
                #     'title': _("Our Brands"),
                #     'brands': Brand.objects.annotate(
                #         product_count=Count('products')
                #     ).filter(product_count__gt=0).order_by('?')[:12]
                # }
            }
            cache.set('home_data', data, 60 * 60 * 24)  # Cache for 1 day
            
        context['data'] = data
        return context['data']


def rate_limit_exceeded(request, exception):
    print(exception)
    return render(request, 'home/rate_limit_exceeded.html', {'exception': exception})
