from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from product.models import Product
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache


@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'profile': request.user.profile})

@ratelimit(key='user', rate='10/m', method='POST', block=False)
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'account/edit_profile.html', {'form': form})

@ratelimit(key='user', rate='40/m', method='POST', block=False)
@require_POST
@login_required
def toggle_wishlist(request):
    try:
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)
        profile = request.user.profile
        cache.delete(f"context_wishlist_{request.user.id}")
        if product in profile.wishlist.all():
            profile.wishlist.remove(product)
            return JsonResponse({'status': 'removed', 'message': _('Removed from wishlist.')})
        else:
            profile.wishlist.add(product)
            return JsonResponse({'status': 'added', 'message': _('Added to wishlist.')})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def remove_wishlist(request,slug):
    product = Product.objects.get(slug=slug)
    profile = request.user.profile
    cache.delete(f"context_wishlist_{request.user.id}")
    if product in profile.wishlist.all() :
        profile.wishlist.remove(product)
        messages.success(request, 'The product has been removed from the wishlist!')
    return redirect("accounts:wishlist")

@ratelimit(key='user', rate='40/m', method='POST', block=False)
@login_required
@require_POST  
def clear_wishlist(request):
    profile = request.user.profile
    profile.wishlist.clear()
    cache.delete(f"context_wishlist_{request.user.id}")
    messages.success(request, _('Wishlist cleared successfully!'))
    return redirect('accounts:wishlist')

@login_required
def view_wishlist(request):
    profile = request.user.profile
    return render(request, 'account/wishlist.html', {'profile': profile})
