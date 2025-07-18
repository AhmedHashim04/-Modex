
from django.core.cache import cache
from django.views.generic import TemplateView
from product.models import Category, Product
from features.models import Collection
from home.models import FeaturedProduct, FeaturedCollection
from django.db.models import Avg
from django.utils.translation import gettext as _
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cache.get('home_data')
        cache.clear()
        if not data:
        

            data = {
                'main_banners': FeaturedCollection.objects.filter(is_active=True).order_by('order')[:20],
                'main_categories': Category.objects.filter(parent__isnull=True, products__isnull=False).distinct()[:8],
                'featured_products_section': {
                    'title': _("Featured Products"), 
                    'products': FeaturedProduct.objects.filter(is_active=True).select_related('product').order_by('order')[:8],
                    'layout': 'carousel'  # يمكن أن يكون 'grid' أو 'carousel'
                },
                'new_products_section': {
                    'title': _("New Arrivals"),
                    'products': Product.objects.filter(is_available=True).order_by('-created_at').select_related('category')[:12],
                    'layout': 'grid'
                },
                'top_rated_section': {
                    'title': _("Top Rated"),
                    'products': Product.objects.filter(is_available=True, overall_rating__gte=4).order_by('-overall_rating')[:12],
                    'layout': 'carousel'
                },
                

                'discounts_section': {
                    'title': _("Hot Deals"),
                    'products': Product.objects.filter(is_available=True, discount__gte=15).order_by('-discount')[:8],
                    'layout': 'carousel'
                },
                

                'collections_section': {
                    'title': _("Our Collections"),
                    'collections': Collection.objects.filter(is_active=True).annotate(
                        product_count=Count('products')
                    ).filter(product_count__gt=0).order_by('-created_at')[:6],
                    'layout': 'grid'
                },
                
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
