from django.db import models
from django.utils.translation import gettext as _





class FeaturedProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='featured_entries')
    offer = models.CharField(_("offer"), max_length=50)
    image = models.ImageField(upload_to='featured_products/', verbose_name="Large Banner Image")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    
    class Meta:
        verbose_name = "Featured Product"
        verbose_name_plural = "Featured Products"
        ordering = ['order', '-created_at']

    def __str__(self):
        return str(self.product)

class FeaturedCollection(models.Model):
    collection = models.ForeignKey('features.Collection', on_delete=models.CASCADE, related_name='featured_entries')
    offer = models.CharField(_("offer"), max_length=50)
    image = models.ImageField(upload_to='featured_collections/', verbose_name="Large Banner Image")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    
    class Meta:
        verbose_name = "Featured Collection"
        verbose_name_plural = "Featured Collections"
        ordering = ['order', '-created_at']

    def __str__(self):
        return str(self.collection)