from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "body"]
    success_url = reverse_lazy("blog:list")


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["title", "body"]
    success_url = reverse_lazy("blog:list")


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
