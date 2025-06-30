from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView, TemplateView
from .forms import ReviewForm
from .models import Product, Review, Category #, Tag
from account.models import Profile
from features.models import Collection#, Brand
from django.db import models
from decimal import Decimal
from django.urls import reverse_lazy
from features.models import Tag
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from django.dispatch import receiver
from ratelimit.decorators import ratelimit
from django_filters.views import FilterView
from .filters import ProductFilter

@method_decorator(ratelimit(key='ip', rate='30/m', block=True), name='dispatch')
class ProductListView(FilterView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 12
    filterset_class = ProductFilter
    strict = False  # ما تظهرش error لو في فلتر غلط
    sort_options = {
        'default': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
        'rating_desc': '-overall_rating',
        'popularity': '-review_count',
    }
    items_per_page_options = [12, 24, 48]
    
    @property
    def applied_filters(self):
        """Extract and sanitize filter parameters"""
        params = self.request.GET.copy()
        cache_key = f"filters_{urlencode(self.request.GET)}"

        if hasattr(self, '_applied_filters'):
            return self._applied_filters
        
        filters = {
            'search': params.get('search', '').strip(),
            'min_price': params.get('min_price', ''),
            'max_price': params.get('max_price', ''),

            'tag': params.get('tag', '').strip(),
            'category': params.get('category', '').strip(),
            # 'brand': params.get('brand', '').strip(),
            'sort_by': params.get('sort_by', 'default'),
            'view_mode': params.get('view_mode', 'grid'),
            'items_per_page': params.get('items_per_page', str(self.paginate_by)),
}
        self._applied_filters = cache.get_or_set(cache_key, filters, 60 * 5)

        return self._applied_filters

    def get_queryset(self):
        """Get optimized queryset with filtering and annotations"""
        if hasattr(self, '_queryset'):
            return self._queryset
    
        cache_key = f"products_{urlencode(self.request.GET)}"

        def get_query():
            # Start with optimized base queryset
            queryset = Product.objects.select_related(
                'category'#, 'brand'
            ).prefetch_related(
                'tags'
            ).filter(
                is_available=True
            ).annotate(
                review_count=Count('reviews')
            )
            filters = self.applied_filters
            # Apply search filter
            if filters['search']:
                queryset = queryset.filter(
                    Q(name__icontains=filters['search']) |
                    Q(description__icontains=filters['search']) |
                    # Q(brand__name__icontains=filters['search'])|
                    Q(category__name__icontains=filters['search']) 
                )
            # Apply category filter
            if filters['category']:
                queryset = queryset.filter(
                    Q(category__slug=filters['category']) |
                    Q(category__parent__slug=filters['category'])
                )

            # Apply tag filter  
            if filters['tag']:
                queryset = queryset.filter(tags__name__iexact=filters['tag']).distinct()

            # Apply brand filter
            # if filters['brand']:
            #     queryset = queryset.filter(brand__slug=filters['brand'])

            # Apply price range filter
            try:
                min_price = float(filters['min_price']) if filters['min_price'] else 0
                queryset = queryset.filter(price__gte=min_price)
            except (ValueError, TypeError):
                pass
            try:
                max_price = Decimal(filters['max_price']) if filters['max_price'] else Decimal('Infinity')
                queryset = queryset.filter(price__lte=max_price)
            except (ValueError, TypeError):
                pass

            # Apply sorting
            sort_field = self.sort_options.get(
                filters['sort_by'], 
                self.sort_options['default']
            )
            return queryset.order_by(sort_field)

        _queryset = cache.get_or_set(cache_key,get_query,60*60*24)  # Cache for 1 day
        return _queryset

    def get_paginate_by(self):
        """Get validated items per page setting"""
        try:
            per_page = int(self.applied_filters['items_per_page'])
            return per_page if per_page in self.items_per_page_options else self.paginate_by
        except (ValueError, TypeError):
            return self.paginate_by

    def get_context_data(self, **kwargs):
        """Add filtering context and aggregations"""
        context = super().get_context_data(**kwargs)
        filters = self.applied_filters
        price_range = cache.get_or_set('global_price_range', lambda:Product.objects.aggregate(
            min_price=models.Min('price'),max_price=models.Max('price')) or 0 ,60*60*24
            )

        queryset = self.get_queryset()

        paginate_by = self.get_paginate_by()
        paginator = Paginator(queryset, paginate_by)
        page_number = self.request.GET.get("page")
        products = paginator.get_page(page_number)

        context['featured_collections'] = Collection.objects.all()

        context.update({
            'categories': Category.objects.prefetch_related('children').all(),
            # 'brands': Brand.objects.all(),
            'tags': Tag.objects.all(),
            'search_query': filters['search'],
            'selected_category': filters['category'],
            'selected_brand': filters['brand'],
            'selected_tag': filters['tag'],
            'sort_by': filters['sort_by'],
            'min_price_filter': filters['min_price'] or price_range['min_price'],
            'max_price_filter': filters['max_price'] or price_range['max_price'],
            'items_per_page': self.get_paginate_by(None),
            'view_mode': filters['view_mode'],
            'sort_options': self.sort_options,
            'items_per_page_options': self.items_per_page_options,
            'global_min_price': price_range['min_price'],
            'global_max_price': price_range['max_price'],
            'products': products,
            'is_paginated': products.has_other_pages(),
        })
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = ReviewForm

    def get_object(self,):
        """Optimize product retrieval with related data"""
        return get_object_or_404(
            # Product.objects.select_related('category', 'brand')
            Product.objects.select_related('category')
                            .prefetch_related('tags', 'reviews__user'),
            slug=self.kwargs['slug']
        )

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and not request.user.is_authenticated:
            login_url = reverse_lazy('account:login')
            return HttpResponseRedirect(f'{login_url}?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        recently_viewed = self.update_recently_viewed(product)
        
        # Get filtered reviews
        reviews = product.reviews.all()
        rating_filter = self.request.GET.get('rating')
        if rating_filter and rating_filter.isdigit() and 1 <= int(rating_filter) <= 5:
            reviews = reviews.filter(rating=int(rating_filter))
        
        # Paginate reviews
        paginator = Paginator(reviews, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get related products (same category)
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).order_by('?')[:4]
        
        product_reviews = Review.objects.filter(product=self.object)
        context.update({
            'review_form': ReviewForm(),
            'reviews': page_obj.object_list,
            'page_obj': page_obj,
            'related_products': related_products,
            'recently_viewed': recently_viewed,
            'rating_filter': rating_filter,
            'product_reviews': product_reviews
        })
        return context

    def update_recently_viewed(self, product):
        """Update session with recently viewed products"""
        session_key = 'recently_viewed'
        viewed = self.request.session.get(session_key, [])
        
        # Remove if exists and add to beginning
        if product.id in viewed:
            viewed.remove(product.id)
        viewed.insert(0, product.id)
        
        # Limit to 6 items
        viewed = viewed[:6]
        self.request.session[session_key] = viewed
        
        # Return products excluding current one
        return Product.objects.filter(id__in=viewed).exclude(id=product.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Create review without saving yet
        review = form.save(commit=False)
        review.user = self.request.user
        review.product = self.object
        
        # Check for existing review
        if Review.objects.filter(user=self.request.user, product=self.object).exists():
            messages.warning(self.request, "You've already reviewed this product!")
            return self.render_to_response(self.get_context_data(form=form))
        
        review.save()
        self.object.update_rating()
        messages.success(self.request, "Thank you for your review!")
        return super().get(self.request)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

class CompareProductsView(TemplateView):
    template_name = 'product/compare_products.html'
    max_products = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slugs = self.request.GET.getlist('product_slug')[:self.max_products]
        
        if len(slugs) < 2:
            raise Http404("Select at least 2 products to compare")
        
        products = Product.objects.filter(slug__in=slugs)
        # Field comparison configuration
        comparable_fields = {
            'name': 'Name',
            'price': 'Price',
            'price_after_discount': 'Discounted Price',
            'overall_rating': 'Rating',
            'review_count': 'Reviews',
            'stock': 'Stock',
            'is_available': 'Availability',
            'category': 'Category',
            'brand': 'Brand',
        }
        
        # Build comparison data
        specifications = []
        for field, label in comparable_fields.items():
            values = []
            for product in products:
                # Handle special fields
                if field == 'price_after_discount':
                    value = getattr(product, 'price_after_discount', None)
                    if value is not None:
                        value = f"{float(value):.2f}"
                elif field == 'price':
                    value = getattr(product, 'price', None)
                    if value is not None:
                        value = f"{float(value):.2f}"
                elif field == 'category':
                    value = product.category.name if product.category else ''
                elif field == 'brand':
                    value = product.brand.name if product.brand else ''
                else:
                    value = getattr(product, field, None)
                
                # Format boolean values
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                
                values.append(value)
            
            specifications.append({
                'name': label,
                'values': values
            })
        
        context.update({
            'products': products,
            'specifications': specifications,
        })
        return context

class WishlistViewDetail(LoginRequiredMixin, TemplateView):
    template_name = 'product/wishlist.html'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        wishlist_products = user_profile.wishlist.select_related('category', 'brand')

        context.update({
            'wishlist_products': wishlist_products,
            'wishlist_count': wishlist_products.count(),
        })
        return context

@login_required
def add_remove_wishlist(request,slug):
    product = Product.objects.get(slug=slug)
    user = get_object_or_404(Profile, user=request.user)
    if product in user.wishlist.all() :
        user.wishlist.remove(product)
        messages.success(request, 'The product has been removed from the wishlist!')
    else:
        user.wishlist.add(product)
        messages.success(request, 'Product added to Wishlist successfully!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def clear_wishlist(request):
    user = get_object_or_404(Profile, user=request.user)
    print("Adsd")
    user.wishlist.clear()
    messages.success(request, 'Wishlist cleared successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def user_see_product(request,slug):
    product = Product.objects.get(slug=slug)
    user = get_object_or_404(Profile, user=request.user)
    if user not in product.viewed_by.all() :
        product.viewed_by.add(user)

    return redirect(product.get_absolute_url())  

@receiver(post_save, sender=Product)
def clear_product_cache(sender, **kwargs):
    cache.delete_pattern("products_*")
