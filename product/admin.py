
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from project.admin import custom_admin_site
from django.core.cache import cache

from .models import Category, Product, Review, ProductImage, ProductColor, Tag

@admin.action(description=_("Export selected products to CSV"))
def export_products_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f"attachment; filename={opts.verbose_name_plural}.csv"
    )
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]

    # Write header
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset.select_related():
        data_row = []
        for field in fields:
            value = getattr(obj, field.name, "")
            if callable(value):
                value = value()
            if isinstance(value, bool):
                value = _(str(value))
            if value is None:
                value = ""
            data_row.append(str(value))
        writer.writerow(data_row)
    return response

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # عدد الفورمات المبدئية


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductColorInline]
    list_display = ("name", "price","category","is_available", "created_at")
    list_filter = ("created_at", "is_available", "category")
    search_fields = ("name", "description", "category__name")
    ordering = ("-created_at",)
    actions = [export_products_to_csv]
    exclude = ('slug',) 
    list_select_related = ("category",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "description")
    list_filter = ("parent",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "content", "rating", "created_at")
    list_filter = ("product", "created_at", "rating")
    search_fields = ("content", "user__username", "product__name")
    ordering = ("-created_at",)
    autocomplete_fields = ["product", "user"]

custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(Review,ReviewAdmin) 
admin.site.register(Tag)
custom_admin_site.register(Tag)
