from django.core.validators import MinValueValidator
from django.db import models

from catalog.utils import NULLABLE
from user.models import User


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
    image = models.ImageField(upload_to="product_image/", verbose_name="Изображение (превью)", **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания (записи в БД)")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата последнего изменения (записи в БД)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return f"{self.title} {self.category} {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

        permissions = [
            ("can_unpublish_product", "Отменять публикацию продукта"),
            ("can_change_any_product_description", "Менять описание любого продукта"),
            ("can_change_any_product_category", "Менять категорию любого продукта"),
        ]

    @property
    def current_version(self):
        return self.versions.all().filter(is_active=True).first()


class Version(models.Model):
    product = models.ForeignKey(
        Product, related_name="versions", on_delete=models.CASCADE, verbose_name="Продукт"
    )  # чтобы обращаться и удалять связанные продукты и версии
    version_number = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="Номер версии")
    version_name = models.CharField(max_length=150, verbose_name="Название версии")
    is_active = models.BooleanField(default=False, verbose_name="Признак текущей версии")

    def __str__(self):
        return f"{self.product} {self.version_number} {self.version_name}"

    class Meta:
        unique_together = ["product", "version_number"]
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
