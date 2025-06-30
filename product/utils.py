from django.utils.text import slugify

def generate_product_slug(name):
    from .models import Product
    base = slugify(name)
    slug = base
    counter = 1

    existing_slugs = set(Product.objects.filter(slug__startswith=base).values_list('slug', flat=True))
    
    while slug in existing_slugs:
        slug = f"{base}-{counter}"
        counter += 1

    return slug
