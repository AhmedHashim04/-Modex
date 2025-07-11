import logging
from decimal import Decimal
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View, FormView
from weasyprint import HTML
from cart.cart import Cart
from .forms import AddressForm, OrderCreateForm
from .models import Address, Order, OrderItem

logger = logging.getLogger(__name__)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create_order.html"
    success_url = reverse_lazy("order:order_list")

    def form_valid(self, form):
        cart = Cart(self.request)
        if not cart:
            form.add_error(None, "Your cart is empty.")
            return super().form_invalid(form)

        try:
            with transaction.atomic():
                order = self._create_order_object(form, cart)
                self._create_order_items(order, cart)
                self.object = order

            # self._schedule_invoice_generation(order)
            self._cleanup_session(cart)
            messages.success(
                self.request,
                "Your order has been placed successfully. "
                "Your invoice is being generated and will be available shortly.",
            )

        except Exception as e:
            logger.exception("Order processing failed")
            form.add_error(None, f"Error processing your order: {str(e)}")
            return super().form_invalid(form)

        return super().form_valid(form)

    def _create_order_object(self, form, cart):
        order = form.save(commit=False)
        order.user = self.request.user
        order.shipping_cost = order.calculate_shipping_cost(weight=0)

        items_total = cart.get_total_price_after_discount()
        tax = cart.get_tax() or Decimal("0.00")
        discount = cart.get_total_discount() or Decimal("0.00")

        order.total_price = max(
            (items_total + order.shipping_cost + tax - discount).quantize(
                Decimal("0.01")
            ),
            Decimal("0.00"),
        )
        order.save()
        return order

    def _create_order_items(self, order, cart):
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )

    # def _schedule_invoice_generation(self, order):
    #     """Schedule PDF generation as async task"""
    #     try:
    #         base_url = self.request.build_absolute_uri("/")

    #         async_task(
    #             "orders.tasks.generate_invoice_pdf",
    #             order.id,
    #             base_url,
    #             hook="orders.tasks.invoice_generation_hook",
    #         )
    #         logger.info("Scheduled invoice generation for order %s", order.id)

    #     except Exception as e:
    #         logger.error(
    #             "Failed to schedule invoice task for order %s: %s", order.id, str(e)
    #         )
    #         # Don't show error to user - order is still valid
    #         # We'll have monitoring for failed tasks

    def _cleanup_session(self, cart):
        """Clean session data after successful order"""
        cart.clear()
        # remove_coupon(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context

class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if order and hasattr(order, "status"):
            order.update_status("cancelled")
        return HttpResponseRedirect(reverse("order:order_detail", args=[order.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.object
        return context

class AddressListCreateView(LoginRequiredMixin, FormView, ListView):
    template_name = "order/address_list_create.html"
    form_class = AddressForm
    success_url = reverse_lazy("order:address")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addresses"] = self.get_queryset()
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user

        if address.is_default:
            Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)

        address.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

