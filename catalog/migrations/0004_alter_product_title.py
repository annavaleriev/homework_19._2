# Generated by Django 5.0.4 on 2024-04-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="title",
            field=models.CharField(max_length=100, verbose_name="наименование"),
        ),
    ]
