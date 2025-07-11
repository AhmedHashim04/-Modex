# Generated by Django 5.2.1 on 2025-07-08 12:28

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=100, verbose_name="Full Name"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=20, verbose_name="Phone Number"),
                ),
                (
                    "address_line",
                    models.CharField(max_length=255, verbose_name="Address Line"),
                ),
                ("city", models.CharField(max_length=100, verbose_name="City")),
                ("country", models.CharField(max_length=100, verbose_name="Country")),
                (
                    "postal_code",
                    models.CharField(max_length=10, verbose_name="Postal Code"),
                ),
                (
                    "is_default",
                    models.BooleanField(default=False, verbose_name="Is Default"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Address",
                "verbose_name_plural": "Addresses",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                            ("cancelled", "Cancelled"),
                            ("returned", "Returned"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("cod", "Cash on Delivery")],
                        default="cod",
                        max_length=20,
                        verbose_name="Payment Method",
                    ),
                ),
                (
                    "shipping_method",
                    models.CharField(
                        choices=[("standard", "Standard Shipping")],
                        default="standard",
                        max_length=20,
                        verbose_name="Shipping Method",
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        verbose_name="Total Price",
                    ),
                ),
                (
                    "status_changed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Status Changed At"
                    ),
                ),
                ("paid", models.BooleanField(default=False, verbose_name="Paid")),
                (
                    "shipping_cost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=8,
                        verbose_name="Shipping Cost",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "invoice_pdf",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="invoices/",
                        verbose_name="Invoice PDF",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="order.address",
                        verbose_name="Shipping Address",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(default=1, verbose_name="Quantity"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Price"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="order.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
        migrations.AddConstraint(
            model_name="address",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_default", True)),
                fields=("user",),
                name="unique_default_address_per_user",
            ),
        ),
    ]
