# Generated by Django 5.2.1 on 2025-07-24 06:46

import django.core.validators
import django.db.models.deletion
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
            name="Profile",
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
                    "phone",
                    models.CharField(
                        blank=True,
                        help_text="Please enter an Egyptian phone number starting with 010, 011, 012, or 015.",
                        max_length=11,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must start with 010, 011, 012, or 015 and be 11 digits.",
                                regex="^(01[0125])[0-9]{8}$",
                            )
                        ],
                        verbose_name="Primary Phone Number",
                    ),
                ),
                (
                    "alternate_phone",
                    models.CharField(
                        blank=True,
                        help_text="You can enter another Egyptian phone number for contact (optional).",
                        max_length=11,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must start with 010, 011, 012, or 015 and be 11 digits.",
                                regex="^(01[0125])[0-9]{8}$",
                            )
                        ],
                        verbose_name="Alternate Phone Number (optional)",
                    ),
                ),
                (
                    "address",
                    models.TextField(
                        blank=True,
                        help_text="Please write your address in detail, e.g., district, building number, apartment number, street name, and any additional details to facilitate order delivery.",
                        verbose_name="Detailed Address",
                    ),
                ),
                (
                    "governorate",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("C", "Cairo"),
                            ("GZ", "Giza"),
                            ("ALX", "Alexandria"),
                            ("ASN", "Aswan"),
                            ("AST", "Assiut"),
                            ("BNS", "Beni Suef"),
                            ("BH", "Beheira"),
                            ("IS", "Ismailia"),
                            ("MN", "Minya"),
                            ("MNF", "Monufia"),
                            ("MT", "Matrouh"),
                            ("KFS", "Kafr El Sheikh"),
                            ("DK", "Dakahlia"),
                            ("SHG", "Sohag"),
                            ("SHR", "Sharqia"),
                            ("PTS", "Port Said"),
                            ("DT", "Damietta"),
                            ("FYM", "Fayoum"),
                            ("GH", "Gharbia"),
                            ("KB", "Qalyubia"),
                            ("LX", "Luxor"),
                            ("WAD", "New Valley"),
                            ("SUZ", "Suez"),
                            ("SIN", "North Sinai"),
                            ("SIS", "South Sinai"),
                            ("QH", "Qena"),
                            ("RSH", "Red Sea"),
                        ],
                        max_length=10,
                        verbose_name="Governorate",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wishlist",
                    models.ManyToManyField(
                        blank=True, related_name="wishlists", to="product.product"
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
    ]
