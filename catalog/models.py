from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(**NULLABLE, verbose_name="описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(**NULLABLE, verbose_name="описание")
    image = models.ImageField(
        upload_to="product_image/", verbose_name="Изображение (превью)", **NULLABLE
    )
    # category = models.ForeignKey(
    #     Category, on_delete=models.CASCADE, verbose_name="категория", **NULLABLE
    # )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="категория",
        **NULLABLE,
        related_name="категории",
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="дата создания (записи в БД)"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="дата последнего изменения (записи в БД)"
    )
    manufactured_at = models.DateField(
        default=None, verbose_name="дата производства продукта"
    )

    def __str__(self):
        return f"{self.title} {self.category} {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
