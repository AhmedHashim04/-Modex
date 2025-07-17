from django.db import models
from django.utils.translation import gettext as _
from product.models import Product
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class ProductImage(models.Model):
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"

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
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="product_colors")
    color = models.CharField(max_length=25, choices=Color.choices)
    product_image = models.OneToOneField("ProductImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

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

# class OfferType(models.TextChoices):
#     PERCENTAGE = "percentage", _("Percentage Discount")
#     FIXED = "fixed", _("Fixed Amount Discount")
#     GIFT = "gift", _("Gift Product")
#     FREE_SHIPPING = "free_shipping", _("Free Shipping")

# class Offer(models.Model):
#     name = models.CharField(max_length=255, verbose_name=_("Offer Name"))
#     description = models.TextField(blank=True, verbose_name=_("Description"))
#     offer_type = models.CharField(max_length=20, choices=OfferType.choices, verbose_name=_("Offer Type"))
#     value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Value"))
#     code = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name=_("Promo Code"))
#     is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
#     start_date = models.DateTimeField(verbose_name=_("Start Date"))
#     end_date = models.DateTimeField(verbose_name=_("End Date"))
#     min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Minimum Order Amount"))
#     max_uses = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Maximum Uses"))
#     used_count = models.PositiveIntegerField(default=0, verbose_name=_("Used Count"))
#     users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name=_("Allowed Users"))
#     products = models.ManyToManyField('product.Product', blank=True, verbose_name=_("Products"))
#     collections = models.ManyToManyField('Collection', blank=True, verbose_name=_("Collections"))

#     class Meta:
#         verbose_name = _("Offer")
#         verbose_name_plural = _("Offers")
#         ordering = ['-start_date']

#     def __str__(self):
#         return self.name

#     def is_valid(self, user=None, order_total=None, now=None):
#         from django.utils import timezone
#         now = now or timezone.now()
#         if not self.is_active:
#             return False
#         if self.start_date and now < self.start_date:
#             return False
#         if self.end_date and now > self.end_date:
#             return False
#         if self.max_uses and self.used_count >= self.max_uses:
#             return False
#         if self.min_order_amount and order_total and order_total < self.min_order_amount:
#             return False
#         if self.users.exists() and user and user not in self.users.all():
#             return False
#         return True