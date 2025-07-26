import pytest
from decimal import Decimal
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import Product, Category, Tag, Review, ProductImage, ProductColor
from PIL import Image
from io import BytesIO
from .factories  import ProductFactory, ReviewFactory
from django.test import override_settings
import tempfile


User = get_user_model()

@pytest.mark.django_db
def test_product_creation_and_defaults():
    product = Product.objects.create(name="TV", price=1000)
    assert product.is_available is True
    assert product.discount == 0
    assert product.slug is not None
    assert product.overall_rating == 0.0

@pytest.mark.django_db
def test_product_slug_generation():
    product = Product.objects.create(name="Smart Phone", price=2000)
    expected_slug = slugify(product.name)
    assert expected_slug in product.slug

@pytest.mark.django_db
def test_product_unique_name():
    Product.objects.create(name="TV", price=1000)
    with pytest.raises(IntegrityError):
        Product.objects.create(name="TV", price=1500)

@pytest.mark.django_db
def test_arabic_name_and_description():
    product = Product.objects.create(
        name="ساعة ذكية", 
        description="أفضل ساعة ذكية بمواصفات ممتازة وسعر مناسب",
        price=1500
    )
    assert product.name == "ساعة ذكية"
    assert "ممتازة" in product.description
    assert product.slug == 's-dhky'

@pytest.mark.django_db
def test_price_after_discount():
    product = Product.objects.create(name="Laptop", price=3500, discount=10)
    assert product.price_after_discount == Decimal("3150.00")

@pytest.mark.django_db
def test_product_str():
    product = Product.objects.create(name="TV", price=1200, is_available=True)
    assert str(product) == "TV - 1200 EGP - Available"

@pytest.mark.django_db
def test_get_absolute_url():
    product = Product.objects.create(name="Camera", price=5000, slug="camera")
    assert product.get_absolute_url() == f"/ar/products/{product.slug}/"

@pytest.mark.django_db
def test_review_creation_and_rating_update():
    user1 = User.objects.create_user(username="ahmed", password="pass")
    user2 = User.objects.create_user(username="mona", password="pass")
    product = Product.objects.create(name="Laptop", price=5000)

    Review.objects.create(product=product, user=user1, content="ممتاز", rating=4)
    Review.objects.create(product=product, user=user2, content="جيد جدًا", rating=5)

    product.update_rating()
    assert product.overall_rating == 4.5

@pytest.mark.django_db
def test_review_unique_constraint():
    user = User.objects.create_user(username="ahmed", password="pass")
    product = Product.objects.create(name="Watch", price=800)
    Review.objects.create(product=product, user=user, content="رائع", rating=5)
    with pytest.raises(IntegrityError):
        Review.objects.create(product=product, user=user, content="تكرار", rating=4)

@pytest.mark.django_db
def test_review_str():
    user = User.objects.create_user(username="testuser", password="pass")
    product = Product.objects.create(name="Book", price=150)
    review = Review.objects.create(product=product, user=user, content="جيد", rating=3)
    assert str(review) == f"{user.username} - {product.name} (3/5)"

@pytest.mark.django_db
def test_image_is_compressed_to_webp(tmp_path):
    img = Image.new("RGB", (1000, 1000), color=(255, 0, 0))
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    image_file = SimpleUploadedFile("test.jpg", buffer.getvalue(), content_type="image/jpeg")

    product = Product.objects.create(name="With Image", price=300, image=image_file)
    assert product.image.name.endswith(".webp")


#--

@pytest.mark.django_db
def test_category_creation_and_slug():
    ar_parent = Category.objects.create(name="الكترونيات")
    ar_child = Category.objects.create(name="هواتف", parent=ar_parent)
    parent = Category.objects.create(name="Electronics")
    child = Category.objects.create(name="Phones", parent=parent)

    assert ar_parent.slug == "lktrwnyt"
    assert ar_child.slug == "hwtf"
    assert parent.slug == "electronics"
    assert child.slug == "phones"
    assert child.parent == parent

def get_test_image(name="test.jpg"):
    from io import BytesIO
    from PIL import Image

    image = Image.new("RGB", (100, 100))
    temp = BytesIO()
    image.save(temp, format="JPEG")
    temp.seek(0)

    return SimpleUploadedFile(name, temp.read(), content_type="image/jpeg")

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
@pytest.mark.django_db
def test_category_image_optimization():
    image = get_test_image()
    cat = Category.objects.create(name="Optimized", image=image)

    assert cat.image.name.endswith(".webp")


@pytest.mark.django_db
def test_product_image_creation_and_compression():
    image = get_test_image()
    product = ProductFactory()
    img = ProductImage.objects.create(product=product, image=image)

    assert img.image.name.endswith(".webp")
    assert img.product == product


@pytest.mark.django_db
def test_product_color_display_and_image():
    image = get_test_image()
    product = ProductFactory()
    color = ProductColor.objects.create(product=product, color="Red", image=image)

    assert color.__str__().endswith("Color: Red") == True
    assert color.image.name.endswith(".webp")


@pytest.mark.django_db
def test_tag_unique_and_ordering():
    tag1 = Tag.objects.create(name="New")
    tag2 = Tag.objects.create(name="Sale")
    tag3 = Tag.objects.create(name="Popular")

    names = list(Tag.objects.values_list("name", flat=True))
    assert sorted(names) == names  # ordering = ['name']

    with pytest.raises(Exception):
        Tag.objects.create(name="New")  # should raise due to unique constraint
