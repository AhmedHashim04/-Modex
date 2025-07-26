import pytest
from product.models import Product

@pytest.mark.django_db
def test_product_discount_price():
    product = Product.objects.create(
        name="iPhone",
        price=1000,
        discount_percentage=20
    )
    assert product.discounted_price == 800  # لو عندك method أو property
