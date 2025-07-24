
import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from slugify import slugify
from faker import Faker
from product.models import Product, Category, Tag, Color,  ProductImage, ProductColor 
from django.db import transaction
from django.core.files.base import ContentFile

fake = Faker("ar_EG")

IMAGE_DIR = "/home/ahmed/Desktop/project/src/media/image_pr"

class Command(BaseCommand):
    help = "Seed products with images and colors"

    def handle(self, *args, **options):
        total = 1000  # اختبر بعدد أقل في البداية
        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        if not image_files:
            self.stdout.write(self.style.ERROR("❌ No images found in the directory."))
            return

        if not categories or not tags:
            self.stdout.write(self.style.ERROR("❌ Categories or Tags missing."))
            return

        created_count = 0
        color_choices = [c[0] for c in Color.choices]

        self.stdout.write("🚀 Starting product creation...")

        with transaction.atomic():
            for _ in range(total):
                category = random.choice(categories)
                name = fake.unique.sentence(nb_words=3).replace(".", "")
                price = round(random.uniform(50, 1000), 2)
                discount = random.choice([0, 5, 10, 15, 20])
                slug = slugify(name) + f"-{random.randint(1000,9999)}"

                product = Product.objects.create(
                    name=name,
                    category=category,
                    description=fake.text(max_nb_chars=300),
                    price=Decimal(price),
                    discount=Decimal(discount),
                    is_available=random.choice([True, True, False]),
                    trending=random.choice([True, False]),
                    slug=slug,
                )

                product.tags.add(*random.sample(tags, random.randint(1, 4)))

                # 📸 Add 3 random product images (first = main image)
                product_images = random.sample(image_files, 3)
                for i, img_file in enumerate(product_images):
                    img_path = os.path.join(IMAGE_DIR, img_file)

                    with open(img_path, "rb") as f:
                        image_data = f.read()
                        django_file = ContentFile(image_data,name=os.path.basename(img_path))

                        if i == 0:
                            product.image.save(img_file, django_file, save=True)
                        else:
                            ProductImage.objects.create(product=product, image=django_file)


                # 🎨 Add 3 random colors with optional images
                for color_code in random.sample(color_choices, 3):
                    color_img_file = random.choice(image_files)
                    color_img_path = os.path.join(IMAGE_DIR, color_img_file)
                    with open(color_img_path, "rb") as f:
                        image_data = f.read()
                        django_file = ContentFile(image_data,name=os.path.basename(img_path))
                        color = ProductColor(product=product, color=color_code)
                        color.image.save(color_img_file, django_file, save=True)
                        color.save()

                created_count += 1
                if created_count % 10 == 0:
                    self.stdout.write(f"✅ Created {created_count} products...")

        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully created {created_count} products with images and colors."))
