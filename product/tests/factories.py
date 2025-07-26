import factory
from product.models import Product, Review
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda x: fake.name())
    description = factory.LazyAttribute(lambda x: fake.text())
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    is_available = True
    trending = False


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(User)
    content = factory.Faker("sentence")
    rating = factory.Iterator([1, 2, 3, 4, 5])
