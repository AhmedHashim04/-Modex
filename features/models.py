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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(max_length=20, choices=Color.choices)
    image = models.ImageField(upload_to=f'products/colors/{product.name}/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.get_color_display()}"

class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"),max_length=100)
    class Meta:
        indexes = [models.Index(fields=["name"])]
    def __str__(self):
        return self.name
