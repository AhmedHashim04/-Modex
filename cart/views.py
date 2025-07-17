import logging
from typing import Any, Dict
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView
from product.models import Product
from .cart import Cart as ShoppingCart

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token

@require_POST
def cart_add(request, slug):
    cart = ShoppingCart(request)
    product = get_object_or_404(Product, slug=slug)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        message = "Invalid quantity specified"
        if is_ajax:
            return JsonResponse({
                'success': False, 
                'message': message,
                'new_csrf_token': get_token(request)
            })
        messages.error(request, message)
        return redirect(referer_url)

    if not (product.is_available and product.is_in_stock):
        message = f"{product.name} is currently unavailable"
        if is_ajax:
            return JsonResponse({
                'success': False, 
                'message': message,
                'new_csrf_token': get_token(request)
            })
        messages.warning(request, message)
        return redirect(referer_url)

    cart.add(product=product, quantity=quantity)
    message = f"{product.name} added to cart successfully"
    
    if is_ajax:
        context = {
            'product': product,
            'contextCart': cart.cart,
            'user': request.user
        }
        updated_html = render_to_string('product/partials/product_card.html', context)
        return JsonResponse({
            'success': True,
            'message': message,
            'updated_html': updated_html,
            'new_csrf_token': get_token(request),
            'cart_count': cart.__len__()
        })
    
    messages.success(request, message)
    referer_url = request.META.get("HTTP_REFERER", reverse("cart:cart_list"))
    if not url_has_allowed_host_and_scheme(referer_url, allowed_hosts={request.get_host()}):
        referer_url = reverse("cart:cart_list")
    return redirect(referer_url)


@require_POST
def cart_remove(request, slug):
    cart = ShoppingCart(request)
    product = get_object_or_404(Product, slug=slug)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    cart.remove(product)
    message = f"{product.name} removed from cart successfully"
    
    if is_ajax:
        context = {
            'product': product,
            'contextCart': cart.cart,
            'user': request.user
        }
        updated_html = render_to_string('product/partials/product_card.html', context)
        return JsonResponse({
            'success': True,
            'message': message,
            'updated_html': updated_html,
            'new_csrf_token': get_token(request),
            'cart_count': cart.__len__()
        })
    
    messages.success(request, message)
    referer_url = request.META.get("HTTP_REFERER", reverse("cart:cart_list"))
    if not url_has_allowed_host_and_scheme(referer_url, allowed_hosts={request.get_host()}):
        referer_url = reverse("cart:cart_list")
    return redirect(referer_url)

@require_POST
def cart_clear(request):
    cart = ShoppingCart(request)
    cart.clear()
    messages.success(request, "Cart cleared successfully")
    return redirect("cart:cart_list")


class CartView(ListView):

    template_name = "cart/cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        return ShoppingCart(self.request)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cart = context["cart"]
        cart_summary = cart.get_cart_summary()

        context.update(
            {
                "cart_summary": cart_summary,
            }
        )
        return context


class CartContextMixin:
    def get_cart(self) -> ShoppingCart:
        try:
            return ShoppingCart(self.request)
        except Exception as e:
            logger.exception("Error loading cart")
            messages.error(
                self.request, "An error occurred while loading the shopping cart."
            )
            return ShoppingCart(self.request)

    def get_cart_summary(self) -> Dict[str, Any]:
        return self.get_cart().get_cart_summary()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.get_cart()
        context["cart_summary"] = self.get_cart_summary()
        return context


class CartView(CartContextMixin, TemplateView):
    template_name = "cart/cart.html"
