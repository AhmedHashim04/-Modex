from decimal import Decimal
from django.conf import settings
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models, transaction
from django.db.models import Avg, UniqueConstraint
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .utils import generate_product_slug


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)
    category = models.ForeignKey("Category",on_delete=models.PROTECT,verbose_name=_("Category"),blank=True,null=True,related_name="products",)
    # brand = models.ForeignKey('features.Brand',on_delete=models.PROTECT,verbose_name=_("Brand"),blank=True,null=True,related_name='products')
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    price = models.DecimalField(max_digits=20,decimal_places=2,verbose_name=_("Price"),validators=[MinValueValidator(0)],)
    # cost = models.DecimalField(max_digits=20,decimal_places=2,verbose_name=_("Cost"),blank=True,null=True,validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="products/", verbose_name=_("Product Image"), blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255, db_index=True)
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"), validators=[MinValueValidator(0)])
    overall_rating = models.FloatField(default=0.0, verbose_name=_("Overall Rating"), editable=False)
    # wishlisted_by = models.ManyToManyField(User,through='features.Wishlist',related_name='wishlist_products')
    is_available = models.BooleanField(default=True, verbose_name=_("Is Available"))
    discount = models.DecimalField(max_digits=5,decimal_places=2,default=0,verbose_name=_("Discount"),help_text=_("Discount percentage (0-100)"),validators=[MinValueValidator(0), MaxValueValidator(100)],)
    trending = models.BooleanField(default=False,verbose_name=_("Trending"),help_text=_("Is this product trending?"),)

    weight = models.DecimalField(max_digits=5,decimal_places=2,verbose_name=_("Weight"),blank=True,null=True,validators=[MinValueValidator(0)],)
    tags = models.ManyToManyField("features.Tag", verbose_name=_("Tags"), blank=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["price"], name="price_idx"),
            models.Index(fields=["-overall_rating"], name="rating_idx"),
            models.Index(fields=["category",],name="category_idx",),
            # models.Index(fields=['category', 'brand'], name='category_brand_idx'),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} EGP - {self.stock} in stock"

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.slug})

    @property
    def price_after_discount(self):
        return (
            self.price
            * (Decimal(100) - self.discount)
            / Decimal(100).quantize(Decimal(".01"))
        )

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def has_discount(self):
        return self.discount > 0

    @property
    def is_on_sale(self):
        return self.price_after_discount < self.price

    def update_rating(self):
        result = self.reviews.aggregate(average_rating=Avg("rating"))
        self.overall_rating = round(result["average_rating"] or 0, 2)
        self.save(update_fields=["overall_rating"])

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = generate_product_slug(self.name)

        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = generate_product_slug(f"{self.name}-{timezone.now().timestamp()}")
            with transaction.atomic():
                super().save(*args, **kwargs)

        # Clear the cache once after save is confirmed
        cache.set("products_", {}, 60 * 5)

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Product"),
    )
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )
    content = models.CharField(
        max_length=255,
        verbose_name=_("Review"),
        help_text=_("Write your feedback here"),
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES, default=3, verbose_name=_("Rating")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"), db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        constraints = [
            UniqueConstraint(fields=["product", "user"], name="unique_product_review")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    parent = models.ForeignKey(
        "self",
        limit_choices_to={"parent__isnull": True},
        on_delete=models.PROTECT,
        verbose_name=_("Parent Category"),
        blank=True,
        null=True,
        related_name="children",
    )
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    image = models.ImageField(
        upload_to="category_pictures/", verbose_name=_("Image"), blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product:category_detail", kwargs={"slug": self.slug})

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """
    Signal receiver that updates the product's rating whenever a review is saved or deleted.

    This function listens to the `post_save` and `post_delete` signals of the `Review` model.
    It recalculates and updates the overall rating of the associated product by calling the
    `update_rating` method on the product instance.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Review): The instance of the review that triggered the signal.
        **kwargs: Additional keyword arguments passed by the signal.
    """
    instance.product.update_rating()
