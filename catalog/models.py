from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(**NULLABLE, verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    image = models.ImageField(
        upload_to="product_image/", verbose_name="Изображение (превью)", **NULLABLE
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения (записи в БД)"
    )

    def __str__(self):
        return f"{self.title} {self.category} {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"