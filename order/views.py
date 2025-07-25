import logging
from decimal import Decimal
from io import BytesIO
from .utils import generate_invoice_pdf
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View, FormView, UpdateView, DeleteView

from cart.cart import Cart
from .forms import AddressForm, OrderCreateForm
from .models import Address, Order, OrderItem
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .tasks import send_order_emails_task, generate_invoice_task


@method_decorator(ratelimit(key='user', rate='20/m', block=True), name='dispatch')
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@method_decorator(ratelimit(key='user', rate='20/m', block=True), name='dispatch')
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='dispatch') #2
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create_order.html"
    success_url = reverse_lazy("order:order_list")

    def form_invalid(self, form):
        print("form_invalid called", form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print("form_valid")
        
        cart = Cart(self.request)
        if len(cart) == 0:
            form.add_error(None, "Your cart is empty.")
            return super().form_invalid(form)

        try:
            with transaction.atomic():
                order = self._create_order_object(form, cart)

                self._create_order_items(order, cart)
                self.object = order

            generate_invoice_task.delay(order.id)
            # self._invoice_generation(order)
            self._cleanup_session(cart)
            messages.success(
                self.request,
                _("Your order has been placed successfully. "
                "Your invoice is being generated and will be available shortly."),
            )

        except Exception as e:
            # logger.exception("Order processing failed")
            print('form error', e)

            form.add_error(None, f"Error processing your order: {str(e)}")
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_initial(self):

        profile = getattr(self.request.user, 'profile', None)
        initial = {
        }
        if profile:
            initial.update({
                'full_name': self.request.user.get_full_name() or self.request.user.username,
                'governorate': profile.governorate,
                'phone': profile.phone,
            })
        return initial


    def _create_order_object(self, form, cart):
        order = form.save(commit=False)
        order.user = self.request.user
        order.shipping_cost = order.calculate_shipping_cost()

        order.shipping_option = form.cleaned_data['shipping_option']

        get_total_price_after_discount = cart.get_total_price_after_discount()
        order.total_price = max(
            (get_total_price_after_discount + order.shipping_cost).quantize(Decimal("0.01")),
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
                discount=item["discount"],
            )

    def _invoice_generation(self, order):
        pdf_content = generate_invoice_pdf(order)
        if pdf_content:
            order.invoice_pdf.save(f"invoice_{order.id}.pdf", ContentFile(pdf_content))
            order.save()
            send_order_emails_task.delay(order.id)

    # def _send_emails(self, order):
    #     context = {
    #         'order': order,
    #         'user': order.user,
    #         'shipping_address': order.address,
    #         'shipping_cost': order.shipping_option,
    #         'total': order.total_price,
    #     }

    #     # 1. 📤 للعميل
    #     subject_customer = f"Thanks for your order #{order.id}"
    #     message_customer = render_to_string("order/order_customer.html", context)
    #     email_customer = EmailMessage(
    #         subject_customer,
    #         message_customer,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [order.user.email],
    #     )
    #     if order.invoice_pdf:
    #         email_customer.attach_file(order.invoice_pdf.path)
    #     email_customer.content_subtype = "html"
    #     email_customer.send()

    #     # 2. 🛒 لصاحب المتجر
    #     subject_owner = f"New Order #{order.id} placed"
    #     message_owner = render_to_string("order/order_store_owner.html", context)
    #     email_owner = EmailMessage(
    #         subject_owner,
    #         message_owner,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [settings.STORE_OWNER_EMAIL],  
    #     )
    #     if order.invoice_pdf:
    #         email_owner.attach_file(order.invoice_pdf.path)
    #     email_owner.content_subtype = "html"
    #     email_owner.send()

    #     # # 3. 🚚 لمسؤول الشحن
    #     # subject_shipping = f"Shipping Info for Order #{order.id}"
    #     # message_shipping = render_to_string("order/order_shipping.html", context)
    #     # email_shipping = EmailMessage(
    #     #     subject_shipping,
    #     #     message_shipping,
    #     #     settings.DEFAULT_FROM_EMAIL,
    #     #     [settings.SHIPPING_EMAIL],  
    #     # )
    #     # email_shipping.content_subtype = "html"
    #     # email_shipping.send()

    def _cleanup_session(self, cart):
        """Clean session data after successful order"""
        cart.clear()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        
        form_class = form_class or self.get_form_class()
        if self.request.method == "POST":
            return form_class(self.request.POST, user=self.request.user)
        return form_class(user=self.request.user, initial=self.get_initial())

@method_decorator(ratelimit(key='user', rate='300/m', block=True), name='dispatch')
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

@method_decorator(ratelimit(key='user', rate='5/m', block=True), name='dispatch')
class AddressEditView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    template_name = "order/address_list_create.html"
    def get_success_url(self):
        messages.success(self.request, "Address updated successfully.")
        return reverse("order:address_list_create")
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    def form_valid(self, form):
        address = form.save(commit=False)
        if address.is_default:
            Address.objects.filter(user=self.request.user, is_default=True).exclude(pk=address.pk).update(is_default=False)
        address.save()
        return super().form_valid(form)

class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = "order/address_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Address deleted successfully.")
        return reverse("order:address_list_create")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class AddressSetDefaultView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        print('updated')
        address.is_default = True
        address.save()
        messages.success(request, "Default address set successfully.")
        return redirect("order:address_list_create")
    def get(self, request, pk):
        return self.post(request, pk)

class AddressUnsetDefaultView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.is_default = False
        address.save()
        messages.success(request, "Default address unset successfully.")
        return redirect("order:address_list_create")
    def get(self, request, pk):
        return self.post(request, pk)

class AddressListCreateView(LoginRequiredMixin, FormView, ListView):
    template_name = "order/address_list_create.html"
    form_class = AddressForm
    success_url = reverse_lazy("order:create_order")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_initial(self):
        profile = getattr(self.request.user, 'profile', None)
        initial = {
        }
        if profile:
            initial.update({
                'governorate': profile.governorate,
                'address_line': profile.address,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addresses"] = self.get_queryset()
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        if self.request.method in ("POST", "PUT"):
            return self.form_class(self.request.POST)
        return self.form_class(initial=self.get_initial())

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
