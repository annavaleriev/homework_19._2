# Generated by Django 4.2.2 on 2024-07-07 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("title", models.CharField(max_length=150, verbose_name="Заголовок")),
                ("slug", models.SlugField()),
                ("body", models.TextField(verbose_name="Содержимое")),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="blog/", verbose_name="Превью"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "published",
                    models.BooleanField(default=True, verbose_name="Признак публикации"),
                ),
                (
                    "views",
                    models.PositiveIntegerField(default=0, verbose_name="Количество просмотров"),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
            },
        ),
    ]
