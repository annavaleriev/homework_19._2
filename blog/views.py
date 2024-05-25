from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleViewMixin:
    model = Article
    fields = ["title", "body"]  # указываем поля, которые будут в форме
    template_name = "blog/article_form.html"

    # def form_valid(self, form): # переопределяем метод form_valid
    #     if form.is_valid(): # проверяем, что форма валидна
    #         new_article = form.save() # сохраняем форму
    #         new_article.slug = slugify(new_article.title) # генерируем slug
    #         new_article.save() # сохраняем изменения
    #     return super().form_valid(form) # вызываем родительский метод form_valid


class ArticleCreateView(ArticleViewMixin,
                        CreateView):  # создаем класс BlogCreateView, который наследуется от CreateView
    success_url = reverse_lazy("blog:list")  # указываем URL, на который будет перенаправлен пользователь после


class ArticleUpdateView(ArticleViewMixin,
                        UpdateView):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse('blog:view', kwargs={'pk': self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен


class ArticleListView(ListView):  # создаем класс BlogListView, который наследуется от ListView
    model = Article  # указываем модель, с которой будет работать наш класс
    template_name = "blog/article_list.html"

    def get_queryset(self, *args, **kwargs):  # тут мы переопределяем метод get_queryset
        queryset = super().get_queryset().order_by(*args,
                                                   **kwargs)  # вызываем родительский метод get_queryset и сортируем его
        queryset = queryset.filter(published=True)  # фильтруем queryset по признаку публикации
        return queryset  # возвращаем отфильтрованный queryset


class ArticleDetailView(DetailView):  # создаем класс BlogDetailView, который наследуется от DetailView
    model = Article
    template_name = "blog/article_detail.html"

    def get_object(self, queryset=None):  # переопределяем метод get_object
        self.object = super().get_object(queryset)  # вызываем родительский метод get_object
        self.object.views += 1  # увеличиваем количество просмотров на 1
        self.object.save()  # сохраняем изменения
        return self.object  # возвращаем объект


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:list")
    template_name = "blog/article_confirm_delete.html"


class ArticleSendEmail:

    @staticmethod
    def send_email(article_ip):
        article = get_object_or_404(Article, pk=article_ip)
        if article.views == 5:
            subject = f"Поздравляю пост {article.title} набрал 100 просмотров "
            message = f"Ты просто милашка! Твой пост {article.title} набрал 100 просмотров"
            from_email = "filenko.a@gmail.com"
            to_email = ["filenko.a@gmail.com"]
            send_mail(subject, message, from_email, to_email)
