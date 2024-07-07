from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from catalog.models import NULLABLE
from django.apps import apps


class UserManager(BaseUserManager):
    """ Класс для создания пользователей"""
    use_in_migrations = True # Переменная для использования в миграциях

    def _create_user(self, email, password, **extra_fields): # Метод для создания пользователя
        if not email: # Если email не указан
            raise ValueError("The given username must be set") # Выводим ошибку
        email = self.normalize_email(email) # Нормализуем email
        GlobalUserModel = apps.get_model(  # Получаем модель пользователя
            self.model._meta.app_label, self.model._meta.object_name  # Получаем модель пользователя
        )
        email = GlobalUserModel.normalize_username(email) # Нормализуем email
        user = self.model(email=email, **extra_fields) # Создаем пользователя
        user.password = make_password(password) # Хешируем пароль
        user.save(using=self._db) # Сохраняем пользователя
        return user # Возвращаем пользователя

    def create_user(self, email, password=None, **extra_fields): # Метод для создания пользователя
        extra_fields.setdefault("is_staff", False) # Устанавливаем значение по умолчанию
        extra_fields.setdefault("is_superuser", False) # Устанавливаем значение по умолчанию
        return self._create_user(email, password, **extra_fields) # Создаем пользователя

    def create_superuser(self, email, password=None, **extra_fields): # Метод для создания суперпользователя
        extra_fields.setdefault("is_staff", True) # Устанавливаем значение по умолчанию
        extra_fields.setdefault("is_superuser", True) # Устанавливаем значение по умолчанию

        if extra_fields.get("is_staff") is not True: # Если пользователь не является сотрудником
            raise ValueError("Superuser must have is_staff=True.") # Выводим ошибку
        if extra_fields.get("is_superuser") is not True: # Если пользователь не является суперпользователем
            raise ValueError("Superuser must have is_superuser=True.") # Выводим ошибку

        return self._create_user(email, password, **extra_fields) # Создаем пользователя


class User(AbstractUser):
    """ Класс для создания пользователей"""
    username = None # Переменная для имени пользователя
    email = models.EmailField(unique=True, verbose_name="Почта") # Поле для почты

    phone = models.CharField(max_length=150, verbose_name="Телефон", **NULLABLE) # Поле для телефона
    avatar = models.ImageField(upload_to="user/", verbose_name="Аватар", **NULLABLE) # Поле для аватара
    country = models.CharField(max_length=150, verbose_name="Страна", **NULLABLE) # Поле для страны

    USERNAME_FIELD = "email" # Поле для имени пользователя
    REQUIRED_FIELDS = [] # Поля, которые обязательны для заполнения

    objects = UserManager() # Объект для работы с пользователями

    def __str__(self):
        return f"{self.email} {self.phone} {self.country}" # Возвращаем строку

    class Meta:
        """ Мета-класс для модели пользователя"""
        verbose_name = "Пользователь" # Название модели в единственном числе
        verbose_name_plural = "Пользователи" # Название модели во множественном числе
