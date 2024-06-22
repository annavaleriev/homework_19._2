from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, FormView, CreateView, UpdateView

from catalog.forms import ContactForm, ProductForm, VersionFormSet, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    """Список продуктов"""
    model = Product
    template_name = "catalog/home.html"

    def get_context_data(self, *, object_list=None,
                         **kwargs):  # переопределяем метод get_context_data для передачи дополнительных данных в контекст
        context = super().get_context_data(object_list=None,
                                           **kwargs)  # получаем контекст из родительского класса ListView
        context["title"] = 'Магазинчик'  # добавляем в контекст новый ключ title со значением 'Магазинчик'
        context[
            "text"] = 'Отличный магазинчик'  # добавляем в контекст новый ключ text со значением 'Отличный магазинчик'

        # context["versions"] = Version.objects.filter(is_active=True).all()

        # for product in context["object_list"]:
        #     product.version = Version.objects.filter(is_active=True, product=product).first()
        # return context
        for product in context["object_list"]: # перебираем все объекты из контекста
            # product.versions = Version.objects.filter(product=product).order_by('version_number')
            product.all_versions = Version.objects.filter(product=product).order_by('version_number')
            # добавляем в объект продукта все версии

        return context # возвращаем контекст


class ContactsTemplateView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Отправка формы"""
        if form.is_valid(): # проверяем валидность формы
            print(form.cleaned_data) # выводим в консоль данные формы
        return super().form_valid(form) # вызываем метод form_valid родительского класса

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляем заголовок на страницу контактов"""
        context = super().get_context_data(object_list=None, **kwargs) # получаем контекст из родительского класса
        context["title"] = 'Контакты' # добавляем в контекст новый ключ title со значением 'Контакты'
        return context # возвращаем контекст


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_info.html"


class ProductMixin:
    model = Product
    form_class = ProductForm # указываем форму, которая будет использоваться
    template_name = "catalog/product_form.html"


class ProductCreateView(ProductMixin,
                        CreateView):  # создаем класс BlogCreateView, который наследуется от CreateView
    success_url = reverse_lazy("catalog:home")  # указываем URL, на который будет перенаправлен пользователь после


class ProductUpdateView(ProductMixin,
                        UpdateView):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse('catalog:product_info', kwargs={'pk': self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен


class VersionListView(ListView):
    model = Version


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm # указываем форму, которая будет использоваться
    success_url = reverse_lazy("catalog:home")


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm # указываем форму, которая будет использоваться
    success_url = reverse_lazy("catalog:home")
