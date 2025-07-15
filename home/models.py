from django.db import models
from django.utils.translation import gettext as _

class FeaturedProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='featured_entries')
    offer = models.CharField(_("offer"), max_length=50)
    image = models.ImageField(upload_to='featured_products/', verbose_name="Large Banner Image")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Featured Product"
        verbose_name_plural = "Featured Products"

    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Limit to 4 featured products: delete oldest if more than 4
        featured = FeaturedProduct.objects.order_by('-created_at')
        if featured.count() > 4:
            # Delete the oldest ones (keep the 4 newest)
            for obj in featured[4:]:
                obj.delete()

class FeaturedCollection(models.Model):
    collection = models.ForeignKey('features.Collection', on_delete=models.CASCADE, related_name='featured_entries')
    offer = models.CharField(_("offer"), max_length=50)
    image = models.ImageField(upload_to='featured_collections/', verbose_name="Large Banner Image")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Featured Collection"
        verbose_name_plural = "Featured Collections"

    def __str__(self):
        return str(self.collection)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Limit to 4 featured collections: delete oldest if more than 4
        featured = FeaturedCollection.objects.order_by('-created_at')
        if featured.count() > 4:
            # Delete the oldest ones (keep the 4 newest)
            for obj in featured[4:]:
                obj.delete()
