import os
import random
from decimal import Decimal
from django.utils.text import slugify
from django.core.files import File
from product.models import Product, Category
from features.models import Tag, Collection, ProductImage, ProductColor, Color
from home.models import FeaturedProduct, FeaturedCollection
from django.db import transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed the database with random data for products, categories, tags, collections, etc., and add featured products and collections."

    def handle(self, *args, **options):
        # Paths for images
        DEFAULT_IMAGE_PATH = os.path.join('static', 'images', 'default.jpg')
        IMAGES_DIR = os.path.join('static', 'imgs')

        # Data counts
        NUM_PRODUCTS = 1000
        NUM_CATEGORIES = 15
        NUM_SUBCATEGORIES = 20
        NUM_TAGS = 30
        NUM_COLLECTIONS = 10
        COLORS = [c[0] for c in Color.choices]

        # Helper functions
        def random_name(prefix):
            return f"{prefix} {random.randint(1000, 9999)}"

        def random_price():
            return Decimal(random.randint(50, 5000))

        def random_description():
            return "Sample product description - Lorem ipsum dolor sit amet."

        def random_stock():
            return random.randint(0, 200)

        def random_discount():
            return Decimal(random.choice([0, 5, 10, 15, 20, 25, 30]))

        def random_weight():
            return Decimal(random.uniform(0.1, 10)).quantize(Decimal('0.01'))

        def get_random_image_path():
            images = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
            if images:
                return os.path.join(IMAGES_DIR, random.choice(images))
            else:
                return DEFAULT_IMAGE_PATH

        # Create main categories
        categories = []
        for i in range(NUM_CATEGORIES):
            categories.append(Category(
                name=f"Category {i+1}",
                description="Main category for products.",
                slug=slugify(f"Category {i+1}"),
            ))
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        categories = list(Category.objects.all()[:NUM_CATEGORIES])

        # Add images to main categories
        for category in categories:
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                category.image.save(f"category_{category.id}.jpg", File(img_file), save=True)

        # Create subcategories
        subcategories = []
        for i in range(NUM_SUBCATEGORIES):
            parent = random.choice(categories)
            subcategories.append(Category(
                name=f"Subcategory {i+1}",
                description="Subcategory for products.",
                parent=parent,
                slug=slugify(f"Subcategory {i+1}"),
            ))
        Category.objects.bulk_create(subcategories, ignore_conflicts=True)
        all_categories = list(Category.objects.all())

        # Add images to subcategories
        for subcategory in all_categories:
            if not subcategory.image:
                image_path = get_random_image_path()
                with open(image_path, 'rb') as img_file:
                    subcategory.image.save(f"category_{subcategory.id}.jpg", File(img_file), save=True)

        # Create tags
        tags = []
        for i in range(NUM_TAGS):
            tags.append(Tag(
                name=f"Tag {i+1}",
                color=random.choice(COLORS),
                bg_color=random.choice(COLORS),
            ))
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        tags = list(Tag.objects.all())

        # Create collections
        collections = []
        for i in range(NUM_COLLECTIONS):
            collections.append(Collection(
                name=f"Collection {i+1}",
                description="Featured product collection.",
                is_active=True,
                is_offer=random.choice([True, False]),
                slug=slugify(f"Collection {i+1}"),
            ))
        Collection.objects.bulk_create(collections, ignore_conflicts=True)
        collections = list(Collection.objects.all())

        # Create products
        products = []
        for i in range(NUM_PRODUCTS):
            products.append(Product(
                name=random_name("Product"),
                description=random_description(),
                price=random_price(),
                stock=random_stock(),
                discount=random_discount(),
                trending=random.choice([True, False]),
                weight=random_weight(),
                category=random.choice(all_categories),
                is_available=True,
                slug=slugify(f"Product{i}"),
            ))
        Product.objects.bulk_create(products, ignore_conflicts=True)
        products = list(Product.objects.all()[:NUM_PRODUCTS])

        # Assign tags to products
        for product in products:
            product.tags.set(random.sample(tags, random.randint(1, 4)))

        # Assign products to collections
        for collection in collections:
            collection.products.set(random.sample(products, random.randint(50, 200)))

        # Add images and colors to products
        product_images = []
        product_colors = []
        for product in products:
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                image_instance = ProductImage(product=product)
                image_instance.image.save(f"product_{product.id}.jpg", File(img_file), save=False)
                product_images.append(image_instance)
            for color in random.sample(COLORS, random.randint(1, 3)):
                product_colors.append(ProductColor(product=product, color=color))
        ProductImage.objects.bulk_create(product_images, ignore_conflicts=True)
        ProductColor.objects.bulk_create(product_colors, ignore_conflicts=True)

        # --- Add Featured Products and Collections (home/models.py) ---
        # Remove all existing featured products/collections to avoid exceeding the limit
        FeaturedProduct.objects.all().delete()
        FeaturedCollection.objects.all().delete()

        # Add up to 4 featured products
        featured_products = random.sample(products, min(4, len(products)))
        for i, product in enumerate(featured_products):
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                fp = FeaturedProduct(
                    product=product,
                    offer=f"Special Offer {i+1}",
                )
                fp.image.save(f"featured_product_{product.id}.jpg", File(img_file), save=True)

        # Add up to 4 featured collections
        featured_collections = random.sample(collections, min(4, len(collections)))
        for i, collection in enumerate(featured_collections):
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                fc = FeaturedCollection(
                    collection=collection,
                    offer=f"Collection Offer {i+1}",
                )
                fc.image.save(f"featured_collection_{collection.id}.jpg", File(img_file), save=True)

        self.stdout.write(self.style.SUCCESS("Data generated successfully, including featured products and collections!"))
