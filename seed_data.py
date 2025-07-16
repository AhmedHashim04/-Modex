import os
import random
from decimal import Decimal
from django.utils.text import slugify
from django.core.files import File
from product.models import Product, Category
from features.models import Tag, Collection, ProductImage, ProductColor, Color
from django.db import transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed the database with random data for products, categories, tags, collections, etc."

    def handle(self, *args, **options):
        # مسار صورة default.jpg
        DEFAULT_IMAGE_PATH = os.path.join('static', 'images', 'default.jpg')

        # مسار مجلد الصور العشوائية
        IMAGES_DIR = os.path.join('static', 'imgs')

        # عدد البيانات المراد توليدها
        NUM_PRODUCTS = 1000
        NUM_CATEGORIES = 15
        NUM_SUBCATEGORIES = 20
        NUM_TAGS = 30
        NUM_COLLECTIONS = 10
        COLORS = [c[0] for c in Color.choices]

        # دوال مساعدة لتوليد بيانات عشوائية

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

        # دالة لاختيار صورة عشوائية من مجلد الصور
        def get_random_image_path():
            images = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
            if images:
                return os.path.join(IMAGES_DIR, random.choice(images))
            else:
                return DEFAULT_IMAGE_PATH

        # توليد التصنيفات الرئيسية
        categories = []
        category_images = []
        for i in range(NUM_CATEGORIES):
            categories.append(Category(
                name=f"Category {i+1}",
                description="Main category for products.",
                slug=slugify(f"Category {i+1}"),
            ))
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        categories = list(Category.objects.all()[:NUM_CATEGORIES])

        # إضافة صور للتصنيفات الرئيسية
        for category in categories:
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                category.image.save(f"category_{category.id}.jpg", File(img_file), save=True)

        # توليد تصنيفات فرعية
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

        # إضافة صور للتصنيفات الفرعية
        for subcategory in all_categories:
            if not subcategory.image:
                image_path = get_random_image_path()
                with open(image_path, 'rb') as img_file:
                    subcategory.image.save(f"category_{subcategory.id}.jpg", File(img_file), save=True)

        # توليد الوسوم (Tags)
        tags = []
        for i in range(NUM_TAGS):
            tags.append(Tag(
                name=f"Tag {i+1}",
                color=random.choice(COLORS),
                bg_color=random.choice(COLORS),
            ))
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        tags = list(Tag.objects.all())

        # توليد التجميعات (Collections)
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

        # توليد المنتجات
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
            ))
        Product.objects.bulk_create(products, ignore_conflicts=True)
        products = list(Product.objects.all()[:NUM_PRODUCTS])

        # ربط المنتجات بالوسوم
        for product in products:
            product.tags.set(random.sample(tags, random.randint(1, 4)))

        # ربط المنتجات بالتجميعات
        for collection in collections:
            collection.products.set(random.sample(products, random.randint(50, 200)))

        # إضافة صور وألوان للمنتجات
        product_images = []
        product_colors = []
        for product in products:
            # إضافة صورة واحدة على الأقل لكل منتج من مجلد imgs
            image_path = get_random_image_path()
            with open(image_path, 'rb') as img_file:
                image_instance = ProductImage(product=product)
                image_instance.image.save(f"product_{product.id}.jpg", File(img_file), save=False)
                product_images.append(image_instance)
            # إضافة ألوان عشوائية لكل منتج
            for color in random.sample(COLORS, random.randint(1, 3)):
                product_colors.append(ProductColor(product=product, color=color))
        ProductImage.objects.bulk_create(product_images, ignore_conflicts=True)
        ProductColor.objects.bulk_create(product_colors, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("Data generated successfully!"))
