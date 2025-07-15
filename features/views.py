
from product.models import Product 

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render, get_object_or_404
from .models import Wishlist, Collection
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'features/collection_detail.html'
    context_object_name = 'collection'
    slug_field = "slug"
    slug_url_kwarg = "slug"


@login_required
def add_to_wishlist(request, product_slug):
    product = Product.objects.only('slug').get(slug=product_slug)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, _('Product added to Wishlist successfully!'))
    else:
        messages.info(request, _('Product is already in your wishlist.'))
    return redirect('product_detail', slug=product_slug)

@login_required
def remove_from_wishlist(request, product_slug):
    product = Product.objects.only('slug').get(slug=product_slug)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, _('The product has been removed from the wishlist!'))
    return redirect('wishlist')

@login_required
def clear_wishlist(request):
    Wishlist.objects.filter(user=request.user).delete()
    messages.success(request, _('Wishlist cleared successfully!'))
    return redirect('wishlist')

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'features/wishlist.html', {'wishlist_items': wishlist_items})



# class CompareProductsView(TemplateView):
#     template_name = 'product/compare_products.html'
#     max_products = 4

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slugs = self.request.GET.getlist('product_slug')[:self.max_products]
        
#         if len(slugs) < 2:
#             raise Http404("Select at least 2 products to compare")
        
#         products = Product.objects.filter(slug__in=slugs)
#         # Field comparison configuration
#         comparable_fields = {
#             'name': 'Name',
#             'price': 'Price',
#             'price_after_discount': 'Discounted Price',
#             'overall_rating': 'Rating',
#             'review_count': 'Reviews',
#             'stock': 'Stock',
#             'is_available': 'Availability',
#             'category': 'Category',
#             'brand': 'Brand',
#         }
        
#         # Build comparison data
#         specifications = []
#         for field, label in comparable_fields.items():
#             values = []
#             for product in products:
#                 # Handle special fields
#                 if field == 'price_after_discount':
#                     value = getattr(product, 'price_after_discount', None)
#                     if value is not None:
#                         value = f"{float(value):.2f}"
#                 elif field == 'price':
#                     value = getattr(product, 'price', None)
#                     if value is not None:
#                         value = f"{float(value):.2f}"
#                 elif field == 'category':
#                     value = product.category.name if product.category else ''
#                 elif field == 'brand':
#                     value = product.brand.name if product.brand else ''
#                 else:
#                     value = getattr(product, field, None)
                
#                 # Format boolean values
#                 if isinstance(value, bool):
#                     value = "Yes" if value else "No"
                
#                 values.append(value)
            
#             specifications.append({
#                 'name': label,
#                 'values': values
#             })
        
#         context.update({
#             'products': products,
#             'specifications': specifications,
#         })
#         return context


# def user_see_product(request,slug):
#     product = Product.objects.get(slug=slug)
#     user = get_object_or_404(Profile, user=request.user)
#     if user not in product.viewed_by.all() :
#         product.viewed_by.add(user)

#     return redirect(product.get_absolute_url())  
