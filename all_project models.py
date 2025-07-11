import uuid
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
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
    PICKUP = "in-store-pickup", _("In-store Pickup")

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("User"))
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    address_line = models.CharField(max_length=255, verbose_name=_("Address Line"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))
    postal_code = models.CharField(max_length=10, verbose_name=_("Postal Code"))
    is_default = models.BooleanField(default=False, verbose_name=_("Is Default"))


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

    def save(self, *args, **kwargs):
        if self.shipping_cost == 0 and self.shipping_method != ShippingMethod.PICKUP:
            self.shipping_cost = Decimal("5.00")
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    parent = models.ForeignKey("self", limit_choices_to={"parent__isnull": True}, on_delete=models.PROTECT, verbose_name=_("Parent Category"), blank=True, null=True, related_name="children")
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    image = models.ImageField(upload_to="category_pictures/", verbose_name=_("Image"), blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            counter = 1
            while Category.objects.filter(slug=base).exists():
                base = f"{slugify(self.name)}-{counter}"
                counter += 1
            self.slug = base
        super().save(*args, **kwargs)
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name=_("Category"), blank=True, null=True, related_name="products")
    # brand = models.ForeignKey('features.Brand',on_delete=models.PROTECT,verbose_name=_("Brand"),blank=True,null=True,related_name='products')
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Price"), validators=[MinValueValidator(0)])
    # cost = models.DecimalField(max_digits=20,decimal_places=2,verbose_name=_("Cost"),blank=True,null=True,validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="products/", verbose_name=_("Product Image"), blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255, db_index=True)
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"), validators=[MinValueValidator(0)])
    overall_rating = models.FloatField(default=0.0, verbose_name=_("Overall Rating"), editable=False)
    wishlisted_by = models.ManyToManyField(User,through='Wishlist',related_name='wishlist_products')
    is_available = models.BooleanField(default=True, verbose_name=_("Is Available"))
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("Discount"), help_text=_("Discount percentage (0-100)"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    trending = models.BooleanField(default=False, verbose_name=_("Trending"), help_text=_("Is this product trending?"))
    tags = models.ManyToManyField("Tag", verbose_name=_("Tags"), blank=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = slugify(self.name + str(timezone.now().timestamp()))
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("Product"))
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="reviews", verbose_name=_("User"))
    content = models.CharField(max_length=255, verbose_name=_("Review"), help_text=_("Write your feedback here"))
    rating = models.IntegerField(choices=RATING_CHOICES, default=3, verbose_name=_("Rating"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product_images/")
class Collection(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField("Product", related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
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
class ProductColor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_colors")
    color = models.CharField(max_length=25, choices=Color.choices)
    product_image = models.OneToOneField("ProductImage", on_delete=models.SET_NULL, null=True, blank=True)
class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    color = models.CharField(choices=Color.choices, max_length=20, blank=True, null=True, verbose_name=_("Color"), help_text=_("Text color for tag (e.g. #fff or 'red')"))
    bg_color = models.CharField(choices=Color.choices, max_length=20, blank=True, null=True, verbose_name=_("Background Color"), help_text=_("Background color for tag (e.g. #000 or 'blue')"))