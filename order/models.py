import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from product.models import Product
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

class ShippingOption(models.Model):
    place = models.CharField(max_length=100, verbose_name=_("place"))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Shipping Price"))
    delivery_time = models.CharField(max_length=100, verbose_name=_("Estimated Delivery Time"))

    class Meta:
        verbose_name = _("Shipping Option")
        verbose_name_plural = _("Shipping Options")

    def __str__(self):
        return f"{self.place} - {self.price} EGP - {self.delivery_time}"


class OrderStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    PROCESSING = "processing", _("Processing")
    SHIPPED = "shipped", _("Shipped")
    DELIVERED = "delivered", _("Delivered")
    CANCELLED = "cancelled", _("Cancelled")
    RETURNED = "returned", _("Returned")
    FAILED = "failed", _("Failed")

class PaymentMethod(models.TextChoices):
    COD = "cod", _("Cash on Delivery")

class ShippingMethod(models.TextChoices):
    STANDARD = "standard", _("Standard Shipping")
    PICKUP = "pickup", _("In-store Pickup")
    # EXPRESS = "express", _("Express Shipping")

class Address(models.Model):
    EGYPT_GOVERNORATES = Profile.EGYPT_GOVERNORATES
    id = models.UUIDField(_("ID"), primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="addresses")
    governorate = models.CharField(max_length=10, choices=EGYPT_GOVERNORATES, verbose_name=_("Governorate"))
    city = models.CharField(max_length=100, verbose_name=_("City/Center"))
    address_line = models.TextField(verbose_name=_("Detailed Address"))
    is_default = models.BooleanField(default=False, verbose_name=_("Default Address"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ["-is_default", "-updated_at"]

    def __str__(self):
        return f" {self.governorate} - {self.city} - {self.address_line}"

class Order(models.Model):
    egyptian_phone_validator = Profile.egyptian_phone_validator

    id = models.UUIDField(_("ID"), primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name=_("User"))
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_("Shipping Address"))
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=11, validators=[egyptian_phone_validator], verbose_name=_("Phone Number"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Additional Notes"))
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name=_("Status"))
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD, verbose_name=_("Payment Method"))
    shipping_method = models.CharField(max_length=20, choices=ShippingMethod.choices, default=ShippingMethod.STANDARD, verbose_name=_("Shipping Method"))

    shipping_option = models.ForeignKey("ShippingOption",on_delete=models.PROTECT,related_name="orders",verbose_name=_("Shipping Option"),null=True,blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Total Price"))
    status_changed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Status Changed At"))
    paid = models.BooleanField(verbose_name=_("Paid"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    invoice_pdf = models.FileField(upload_to="invoices/", null=True, blank=True, verbose_name=_("Invoice PDF"))

    def get_items(self):
        return self.items.all()

    def update_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.status_changed_at = timezone.now()
            self.save()

    def calculate_shipping_cost(self):
        if self.shipping_option:
            return self.shipping_option.price
        return Decimal("0.00")


    def clean(self):
        if self.total_price < 0 or self.shipping_cost < 0:
            raise ValidationError(_("Prices must be non-negative."))

    def save(self, *args, **kwargs):
        if self.shipping_cost == 0 and self.shipping_method != ShippingMethod.PICKUP:
            self.shipping_cost = self.calculate_shipping_cost()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Discount"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
    @property
    def total_item_price_after_discount(self):
        return self.quantity * self.price * (1 - self.discount / 100)