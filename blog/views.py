from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleViewMixin:
    """Миксин для формы статьи"""
    model = Article
    fields = ["title", "body", "image"]  # указываем поля, которые будут в форме
    template_name = "blog/article_form.html"


class ArticleCreateView(ArticleViewMixin,
                        CreateView):  # создаем класс BlogCreateView, который наследуется от CreateView
    """Создание статьи"""
    success_url = reverse_lazy("blog:list")  # указываем URL, на который будет перенаправлен пользователь после


class ArticleUpdateView(ArticleViewMixin,
                        UpdateView):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    """Редактирование статьи"""

    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse('blog:view', kwargs={'pk': self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен


class ArticleListView(ListView):  # создаем класс BlogListView, который наследуется от ListView
    """Список статей"""
    model = Article  # указываем модель, с которой будет работать наш класс
    template_name = "blog/article_list.html"  # указываем имя шаблона, который будет использоваться

    def get_queryset(self, *args, **kwargs):  # тут мы переопределяем метод get_queryset
        """Получаем queryset и фильтруем его по признаку публикации"""
        queryset = super().get_queryset().order_by(*args,
                                                   **kwargs)  # вызываем родительский метод get_queryset и сортируем его
        queryset = queryset.filter(published=True)  # фильтруем queryset по признаку публикации
        return queryset  # возвращаем отфильтрованный queryset


class ArticleDetailView(DetailView):  # создаем класс BlogDetailView, который наследуется от DetailView
    """Просмотр статьи"""
    model = Article
    template_name = "blog/article_detail.html"  # указываем имя шаблона, который будет использоваться

    def send_info_about_views(self):
        """Отправляем письмо при 100 просмотрах"""
        subject = f"Поздравляю пост {self.object.title} набрал 100 просмотров "
        message = f"Ты просто милашка! Твой пост {self.object.title} набрал 100 просмотров"
        from_email = settings.EMAIL_HOST_USER
        to_email = ["filenko.a@gmail.com"]
        try:
            send_mail(subject, message, from_email, to_email)
        except SMTPException as e:
            print(e)

    def get_object(self, queryset=None):  # переопределяем метод get_object
        """Получаем объект и увеличиваем количество просмотров на 1"""
        self.object = super().get_object(queryset)  # вызываем родительский метод get_object
        self.object.views += 1  # увеличиваем количество просмотров на 1
        self.object.save()  # сохраняем изменения
        if self.object.views > settings.COUNT_VIEWS_FOR_SEND_EMAIL:  # если количество просмотров больше 100
            self.send_info_about_views()  # отправляем письмо
        return self.object  # возвращаем объект


class ArticleDeleteView(DeleteView):
    """Удаление статьи"""
    model = Article
    success_url = reverse_lazy("blog:list")  # указываем URL, на который будет перенаправлен пользователь после
    template_name = "blog/article_confirm_delete.html"  # указываем имя шаблона, который будет использоваться
