# Generated by Django 4.2.2 on 2024-07-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_product_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "permissions": [
                    ("can_unpublish_product", "Can unpublish product"),
                    ("can_change_any_product_description", "Can change any product description"),
                    ("can_change_any_product_category", "Can change any product category"),
                ],
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]
