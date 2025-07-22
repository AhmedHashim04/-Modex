import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from slugify import slugify
from faker import Faker
from product.models import Product, Category
from features.models import Tag
from django.db import transaction

fake = Faker("ar_EG")  # Arabic faker

class Command(BaseCommand):
    help = "Seed 20,000 dummy products using existing categories and tags (no images)"

    def handle(self, *args, **options):
        total = 20_000
        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        if not categories:
            self.stdout.write(self.style.ERROR("❌ No categories found."))
            return

        if not tags:
            self.stdout.write(self.style.ERROR("❌ No tags found."))
            return

        created_count = 0

        self.stdout.write("🚀 Starting product creation...")

        with transaction.atomic():
            for _ in range(total):
                category = random.choice(categories)
                name = fake.unique.sentence(nb_words=3).replace(".", "")
                price = round(random.uniform(50, 1000), 2)
                discount = random.choice([0, 5, 10, 15, 20, 25, 30])
                slug = slugify(name) + f"-{random.randint(1000,9999)}"

                product = Product(
                    name=name,
                    category=category,
                    description=fake.text(max_nb_chars=300),
                    price=Decimal(price),
                    discount=Decimal(discount),
                    is_available=random.choice([True, True, False]),
                    trending=random.choice([True, False]),
                    slug=slug,
                )
                product.save()

                selected_tags = random.sample(tags, random.randint(1, 5))
                product.tags.add(*selected_tags)

                created_count += 1
                if created_count % 1000 == 0:
                    self.stdout.write(f"✅ Created {created_count} products...")

        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully created {created_count} products with tags."))
