import uuid
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models, transaction
from django.db.models import Avg, Q, UniqueConstraint
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from product.models import Product
from product.utils import generate_product_slug


# accounts/models.py
class Profile(models.Model):
    EGYPT_GOVERNORATES = [
        ('C', 'القاهرة'),
        ('GZ', 'الجيزة'),
        ('ALX', 'الإسكندرية'),
        ('ASN', 'أسوان'),
        ('AST', 'أسيوط'),
        ('BNS', 'بني سويف'),
        ('BH', 'البحيرة'),
        ('IS', 'الإسماعيلية'),
        ('MN', 'المنيا'),
        ('MNF', 'المنوفية'),
        ('MNFY', 'المنوفية'),
        ('MT', 'مطروح'),
        ('KFS', 'كفر الشيخ'),
        ('DK', 'الدقهلية'),
        ('SHG', 'سوهاج'),
        ('SHR', 'الشرقية'),
        ('PTS', 'بورسعيد'),
        ('DT', 'دمياط'),
        ('FYM', 'الفيوم'),
        ('GH', 'الغربية'),
        ('KB', 'القليوبية'),
        ('LX', 'الأقصر'),
        ('WAD', 'الوادي الجديد'),
        ('SUZ', 'السويس'),
        ('SIN', 'شمال سيناء'),
        ('SIS', 'جنوب سيناء'),
        ('QH', 'قنا'),
        ('RSH', 'البحر الأحمر'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    governorate = models.CharField(
        max_length=10,
        choices=EGYPT_GOVERNORATES,
        blank=True,
        verbose_name="المحافظة"
    )

    def __str__(self):
        return self.user.username

# features/models.py
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user} ♥ {self.product}"

# product/models.py
class ProductImage(models.Model):
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"

# features/models.py
class Collection(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField("product.Product", related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)
    is_offer = models.BooleanField(default=False,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

        indexes = [
        models.Index(fields=["created_at"]),
        models.Index(fields=["is_active"]),
    ]

    def __str__(self):
        return self.name

# product/models.py
class Color(models.TextChoices):
    BEIGE = "#f5f5dc", _("Beige")
    BLACK = "#000", _("Black")
    BLUE = "#00f", _("Blue")
    BROWN = "#a52a2a", _("Brown")
    CORAL = "#ff7f50", _("Coral")
    CYAN = "#00ffff", _("Cyan")
    GOLD = "#ffd700", _("Gold")
    GRAY = "#808080", _("Gray")
    GREEN = "#0f0", _("Green")
    INDIGO = "#4b0082", _("Indigo")
    LAVENDER = "#e6e6fa", _("Lavender")
    LIME = "#00ff00", _("Lime")
    MAGENTA = "#ff00ff", _("Magenta")
    MAROON = "#800000", _("Maroon")
    MINT = "#98ff98", _("Mint")
    NAVY = "#000080", _("Navy")
    OLIVE = "#808000", _("Olive")
    ORANGE = "#ffa500", _("Orange")
    PINK = "#ffc0cb", _("Pink")
    PURPLE = "#800080", _("Purple")
    RED = "#f00", _("Red")
    SALMON = "#fa8072", _("Salmon")
    SILVER = "#c0c0c0", _("Silver")
    TEAL = "#008080", _("Teal")
    TURQUOISE = "#40e0d0", _("Turquoise")
    VIOLET = "#ee82ee", _("Violet")
    WHITE = "#fff", _("White")
    YELLOW = "#ff0", _("Yellow")

# product/models.py
class ProductColor(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="product_colors")
    color = models.CharField(max_length=25, choices=Color.choices)
    product_image = models.OneToOneField("ProductImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

# features/models.py
class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"),max_length=100)
    color = models.CharField(choices=Color.choices,max_length=20,blank=True,null=True, 
                                verbose_name=_("Color"),help_text=_("Text color for tag (e.g. #fff or 'red')"))
    bg_color = models.CharField(choices=Color.choices,max_length=20,blank=True,null=True,
                                verbose_name=_("Background Color"),help_text=_("Background color for tag (e.g. #000 or 'blue')"),)
    class Meta:
        indexes = [models.Index(fields=["name"])]
    def __str__(self):
        return self.name

# order/models.py
class OrderStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    PROCESSING = "processing", _("Processing")
    SHIPPED = "shipped", _("Shipped")
    DELIVERED = "delivered", _("Delivered")
    CANCELLED = "cancelled", _("Cancelled")
    RETURNED = "returned", _("Returned")
    FAILED = "failed", _("Failed")

# order/models.py
class PaymentMethod(models.TextChoices):
    COD = "cod", _("Cash on Delivery")

# order/models.py
class ShippingMethod(models.TextChoices):
    STANDARD = "standard", _("Standard Shipping")
    PICKUP = "pickup", _("In-store Pickup")
    # EXPRESS = "express", _("Express Shipping")

# order/models.py
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

# order/models.py
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

# order/models.py
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
