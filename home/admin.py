from django.contrib import admin
from .models import FeaturedProduct, FeaturedCollection

# Register your models here.
admin.site.register(FeaturedProduct)
admin.site.register(FeaturedCollection)
