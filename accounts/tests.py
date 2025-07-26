from django.test import TestCase

from .models import Product

def test_discount_price():
    product = Product(price=100, discount=0.2)
    assert product.get_discount_price() == 80