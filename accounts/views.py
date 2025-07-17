from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from product.models import Product


@login_required
def check_profile_completion(request):
    profile = request.user.profile

    if not profile.address or not profile.phone or not profile.governorate:
        return redirect('edit_profile')
    else:
        return redirect('home')  # غيّرها حسب المكان اللي عايز توديه بعد التأكد

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'account/profile.html', {'profile': request.user.profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'account/edit_profile.html', {'form': form})


@require_POST
@login_required
def toggle_wishlist(request):
    try:
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)
        profile = request.user.profile

        if product in profile.wishlist.all():
            profile.wishlist.remove(product)
            return JsonResponse({'status': 'removed', 'message': _('Removed from wishlist.')})
        else:
            profile.wishlist.add(product)
            return JsonResponse({'status': 'added', 'message': _('Added to wishlist.')})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def clear_wishlist(request):
    profile = request.user.profile
    profile.wishlist.clear()
    messages.success(request, _('Wishlist cleared successfully!'))
    return redirect('accounts:wishlist')

@login_required
def view_wishlist(request):
    return render(request, 'account/wishlist.html')
