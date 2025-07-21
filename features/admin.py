from django.contrib import admin

from .models import ProductImage, ProductColor, Tag
from project.admin import custom_admin_site

admin.site.register(Tag)
custom_admin_site.register(Tag)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # عدد الفورمات المبدئية


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1

