# Generated by Django 5.2.1 on 2025-07-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0002_remove_product_category_idx_alter_product_created_at_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="overall_rating",
            field=models.FloatField(default=0.0, verbose_name="Overall Rating"),
        ),
    ]
