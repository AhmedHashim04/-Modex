from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from product.models import Product
from django.conf import settings
from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # مايتكررش نفس المنتج لنفس المستخدم

    def __str__(self):
        return f"{self.user} ♥ {self.product}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    products = models.ManyToManyField("product.Product", related_name="collections")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.name


class Colors(models.TextChoices):
    BLACK = "#000", _("Black")
    WHITE = "#fff", _("White")
    RED = "#f00", _("Red")
    GREEN = "#0f0", _("Green")
    BLUE = "#00f", _("Blue")
    YELLOW = "#ff0", _("Yellow")
    ORANGE = "#ffa500", _("Orange")
    PINK = "#ffc0cb", _("Pink")
    PURPLE = "#800080", _("Purple")
    BROWN = "#a52a2a", _("Brown")
    GRAY = "#808080", _("Gray")
    SILVER = "#c0c0c0", _("Silver")
    GOLD = "#ffd700", _("Gold")
    BEIGE = "#f5f5dc", _("Beige")
    CYAN = "#00ffff", _("Cyan")
    MAGENTA = "#ff00ff", _("Magenta")
    LIME = "#00ff00", _("Lime")
    NAVY = "#000080", _("Navy")
    TEAL = "#008080", _("Teal")
    MAROON = "#800000", _("Maroon")
    OLIVE = "#808000", _("Olive")
    INDIGO = "#4b0082", _("Indigo")
    VIOLET = "#ee82ee", _("Violet")
    TURQUOISE = "#40e0d0", _("Turquoise")
    CORAL = "#ff7f50", _("Coral")
    SALMON = "#fa8072", _("Salmon")
    MINT = "#98ff98", _("Mint")
    LAVENDER = "#e6e6fa", _("Lavender")


class ProductColors(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors"
    )
    color = models.CharField(max_length=20, choices=Colors.choices)
    image = models.OneToOneField(
        "ProductImage", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.color}"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.product.slug})


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Color"),
        help_text=_("Text color for tag (e.g. #fff or 'red')"),
    )
    bg_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Background Color"),
        help_text=_("Background color for tag (e.g. #000 or 'blue')"),
    )

    def __str__(self):
        return self.name


# class NewsletterSubscriber(models.Model):
#     email = models.EmailField(unique=True)
#     subscribed_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     class Meta:
#         verbose_name = "Newsletter Subscriber"
#         verbose_name_plural = "Newsletter Subscribers"
#     def __str__(self):
#         return self.email
