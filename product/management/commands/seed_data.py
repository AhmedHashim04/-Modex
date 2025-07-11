# core/management/commands/seed.py
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from django.contrib.auth.models import User
from accounts.models import Profile
from product.models import Category, Product, Review
from features.models import Tag, Wishlist, Collection, ProductImage, ProductColor, Color
from order.models import Address, Order, OrderItem, OrderStatus, ShippingMethod
class Command(BaseCommand):
    help = 'Adds fake data to the database with custom counts'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users')
        parser.add_argument('--categories', type=int, default=5, help='Number of categories')
        parser.add_argument('--products', type=int, default=20, help='Number of products')
        parser.add_argument('--tags', type=int, default=15, help='Number of tags')
        parser.add_argument('--addresses', type=int, default=30, help='Number of addresses')
        parser.add_argument('--orders', type=int, default=50, help='Number of orders')
        parser.add_argument('--reviews', type=int, default=100, help='Number of reviews')
        parser.add_argument('--collections', type=int, default=8, help='Number of collections')
        parser.add_argument('--wishlists', type=int, default=70, help='Number of wishlist items')

    def handle(self, *args, **options):
        fake = Faker()
        seeder = Seed.seeder()

        # 1. إنشاء المستخدمين والملفات الشخصية
        seeder.add_entity(User, options['users'], {
            'username': lambda x: fake.unique.user_name(),
            'email': lambda x: fake.unique.email(),
            'password': 'pbkdf2_sha256$600000$fake_password$='
        })
        user_pks = seeder.execute()[User]
        for user in User.objects.filter(id__in=user_pks):
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.phone = fake.phone_number()[:15]
                profile.address = fake.address()
                profile.save()

            

        # 2. إنشاء الفئات
        seeder.add_entity(Category, options['categories'], {
            'name': lambda x: fake.unique.word().title(),
            'description': lambda x: fake.text(max_nb_chars=200),
        })
        category_pks = seeder.execute()[Category]

        # 3. إنشاء العلامات
        seeder.add_entity(Tag, options['tags'], {
            'name': lambda x: fake.unique.word().title(),
            'color': lambda x: random.choice(Color.values)[0],
            'bg_color': lambda x: random.choice(Color.values)[0]
        })
        tag_pks = seeder.execute()[Tag]

        # 4. إنشاء المنتجات
        seeder.add_entity(Product, options['products'], {
            'name': lambda x: fake.unique.sentence(nb_words=3),
            'category': lambda x: random.choice(Category.objects.all()),
            'description': lambda x: fake.text(max_nb_chars=200),
            'price': lambda x: Decimal(random.uniform(10, 1000)),
            'stock': lambda x: random.randint(0, 100),
            'discount': lambda x: random.randint(0, 50)
        })
        product_pks = seeder.execute()[Product]
        Product._meta.local_many_to_many = []
        
        # إضافة العلامات للمنتجات
        tags = Tag.objects.all()
        for product in Product.objects.filter(id__in=product_pks):
            product.tags.set(random.sample(list(tags), random.randint(1, 3)))
            
            # إنشاء صور للمنتج
            for _ in range(random.randint(1, 4)):
                ProductImage.objects.create(
                    product=product,
                    image=f'products/{fake.file_name(extension="jpg")}'
                )
                    
        # إنشاء ألوان للمنتج بدون تكرار الصور
        images = list(product.product_images.all())
        used_images = set()

        for color in random.sample(Color.values, random.randint(1, 3)):
            available_images = [img for img in images if img.id not in used_images]

            if not available_images:
                break  # كل الصور اتستخدمت

            chosen_image = random.choice(available_images)
            used_images.add(chosen_image.id)

            ProductColor.objects.create(
                product=product,
                color=color[0],
                product_image=chosen_image
            )

        # 5. إنشاء العناوين
        users = User.objects.all()
        seeder.add_entity(Address, options['addresses'], {
            'user': lambda x: random.choice(users),
            'full_name': lambda x: fake.name(),
            'phone_number': lambda x: fake.phone_number(),
            'address_line': lambda x: fake.street_address(),
            'city': lambda x: fake.city(),
            'country': lambda x: fake.country(),
            'postal_code': lambda x: fake.postcode(),
            'is_default': lambda x: fake.boolean(chance_of_getting_true=25)

        })
        address_pks = seeder.execute()[Address]

        # 6. إنشاء الطلبات
        addresses = Address.objects.all()
        seeder.add_entity(Order, options['orders'], {
            'user': lambda x: random.choice(users),
            'address': lambda x: random.choice(addresses),
            'status': lambda x: random.choice(OrderStatus.values)[0],
            'shipping_method': lambda x: random.choice(ShippingMethod.values)[0],
            'total_price': lambda x: Decimal(random.uniform(50, 2000)),
            'shipping_cost': lambda x: Decimal(random.uniform(5, 50))
        })
        order_pks = seeder.execute()[Order]

        # 7. إنشاء عناصر الطلب
        orders = Order.objects.all()
        products = Product.objects.all()
        for order in orders:
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 10),
                    price=product.price
                )

        # 8. إنشاء التقييمات
        seeder.add_entity(Review, options['reviews'], {
            'product': lambda x: random.choice(products),
            'user': lambda x: random.choice(users),
            'content': lambda x: fake.sentence(nb_words=6),
            'rating': lambda x: random.randint(1, 5)
        })
        seeder.execute()

        # # 9. إنشاء القوائم المفضلة
        # seeder.add_entity(Wishlist, options['wishlists'], {
        #     'user': lambda x: random.choice(users),
        #     'product': lambda x: random.choice(products)
        # })
        # seeder.execute()

        # 10. إنشاء المجموعات
# إنشاء المجموعات بدون products
        collection_pks = []
        for _ in range(options['collections']):
            collection = Collection.objects.create(
                name=fake.unique.sentence(nb_words=2),
                description=fake.text(max_nb_chars=200),
        )
        collection_pks.append(collection.pk)

        
        # إضافة منتجات للمجموعات
        collections = Collection.objects.all()
        for collection in collections:
            collection.products.set(random.sample(list(products), random.randint(5, 15)))

        self.stdout.write(self.style.SUCCESS('✅ تم إنشاء البيانات بنجاح!'))