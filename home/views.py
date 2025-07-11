
from django.core.cache import cache
from django.views.generic import TemplateView
from product.models import Category, Product
from features.models import Collection
from django.db.models import Avg


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cache.get('home_data')
        if not data:
            data = {
                
                'newCollections': Collection.objects.filter(is_active=True)[:3],
                'randomCollections': Collection.objects.filter(is_active=True)[:9],
                'mainCategories': Category.objects.filter(parent__isnull=True),
                'subCategories': Category.objects.filter(parent__isnull=False),
                'topRatedProducts': Product.objects.order_by('-overall_rating')[:20],
                'newProducts': Product.objects.order_by('-created_at')[:30],
                'trendingProducts': Product.objects.filter(trending=True)[:20],
                'recommendedProducts': Product.objects.annotate(avg_rating=Avg('reviews__rating'))
                    .order_by('-avg_rating')[:12],

                'randomProducts': Product.objects.order_by('?')[:20],
                'randomProduct' : Product.objects.order_by('?').first()
            }
            cache.set('home_data', data, 60 * 60 * 24)  # Cache for 1 day
            
        context['data'] = data
        return context['data']

