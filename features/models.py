from django.db import models
from django.utils.translation import gettext as _
from product.models import Product
from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        unique_together = ('user', 'product')  

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
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField("product.Product", related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)

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
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="product_colors")
    color = models.CharField(max_length=25, choices=Color.choices)
    product_image = models.OneToOneField("ProductImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"),max_length=100)
    color = models.CharField(
        choices=Color.choices,
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Color"),
        help_text=_("Text color for tag (e.g. #fff or 'red')"),
    )
    bg_color = models.CharField(
        choices=Color.choices,
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Background Color"),
        help_text=_("Background color for tag (e.g. #000 or 'blue')"),
    )
    class Meta:
        indexes = [models.Index(fields=["name"])]
    def __str__(self):
        return self.name
