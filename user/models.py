from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")

    phone = models.CharField(max_length=150, verbose_name="Телефон", **NULLABLE)
    avatar = models.ImageField(upload_to="user/", verbose_name="Аватар", **NULLABLE)
    country = models.CharField(max_length=150, verbose_name="Страна", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email, self.phone, self.country

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
