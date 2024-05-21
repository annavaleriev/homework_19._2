from django.db import models
from django.db.models import F

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.GeneratedField(
        expression=F("title"),
        output_field=models.CharField(max_length=150, unique=True, verbose_name="Slug", **NULLABLE),
        db_persist=True,
    )
    body = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(verbose_name="Превью", upload_to="blog/", **NULLABLE)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    published = models.BooleanField(verbose_name="Признак публикации", default=True)
    views = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
