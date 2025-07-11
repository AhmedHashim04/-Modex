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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("User"))
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    address_line = models.CharField(max_length=255, verbose_name=_("Address Line"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))
    postal_code = models.CharField(max_length=10, verbose_name=_("Postal Code"))
    is_default = models.BooleanField(default=False, verbose_name=_("Is Default"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_default=True),
                name="unique_default_address_per_user"
            )
        ]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"

class Order(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name=_("User"))
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_("Shipping Address"))
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name=_("Status"))
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD, verbose_name=_("Payment Method"))
    shipping_method = models.CharField(max_length=20, choices=ShippingMethod.choices, default=ShippingMethod.STANDARD, verbose_name=_("Shipping Method"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Total Price"))
    status_changed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Status Changed At"))
    paid = models.BooleanField(verbose_name=_("Paid"), default=False)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_("Shipping Cost"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    invoice_pdf = models.FileField(upload_to="invoices/", null=True, blank=True, verbose_name=_("Invoice PDF"))

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order {self.id} - {self.user.email if self.user else 'Anonymous'}"

    def get_items(self) -> models.QuerySet:
        return self.items.all()

    def update_status(self, new_status: str):
        if self.status != new_status:
            self.status = new_status
            self.status_changed_at = timezone.now()
            self.save()

    def calculate_shipping_cost(self, weight: float = 1.0) -> Decimal:
        if self.shipping_method == ShippingMethod.STANDARD:
            return Decimal("5.00") + Decimal(weight) * Decimal("0.50")
        elif self.shipping_method == ShippingMethod.EXPRESS:
            return Decimal("10.00") + Decimal(weight) * Decimal("1.00")
        elif self.shipping_method == ShippingMethod.PICKUP:
            return Decimal("0.00")
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

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"