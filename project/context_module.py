from cart.cart import Cart as ShoppingCart
from product.models import Category

# from features.models import Brand


from django.core.cache import cache
from accounts.models import Profile

#هيتعرض في كل صفحة عايزه يعمل اقل قدر من ال query
#شوف اوقات ال كاش كدا مناسبة 

def contexts(request):
    # cache.clear()
    context = {}

    categories = cache.get('context_categories')
    if categories is None:
        categories = Category.objects.filter(parent=None)[:10]
        cache.set('context_categories', categories, 60 * 60 * 24) # كاش يوم

    cart = ShoppingCart(request)

    profile = None
    wishlist = None
    
    if request.user.is_authenticated:
        profile_cache_key = f"context_profile_{request.user.id}"
        wishlist_cache_key = f"context_wishlist_{request.user.id}"

        profile = cache.get(profile_cache_key)
        wishlist = cache.get(wishlist_cache_key)

        if profile is None:
            try:
                profile = Profile.objects.get(user=request.user.id)
                cache.set(profile_cache_key, profile, 60 * 60 * 6)  # كاش 6 ساعات
            except Profile.DoesNotExist:
                profile = None

        if wishlist is None and profile is not None:
            wishlist = profile.wishlist.all()
            cache.set(wishlist_cache_key, wishlist, 60 * 60 * 2)  # كاش ساعتين
        context["contextProfile"] = profile
        context["contextWishlist"] = wishlist


    context.update({
        "contextCategories": categories,
        "contextCart": cart.cart.keys(),
        "total_cart_price": cart.get_total_price_after_discount(),
        "total_cart_items": len(cart.cart.keys()),
    })


    return context
