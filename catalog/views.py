from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from catalog.forms import ContactForm, UpdateProductForm
from catalog.mixins import IsPublishedQuerysetMixin, ProductMixin
from catalog.models import Product, Version


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, IsPublishedQuerysetMixin, ListView):
    """Список продуктов"""

    model = Product
    template_name = "catalog/home.html"
    permission_required = "catalog.view_product"

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.has_perm(self.permission_required):
    #         messages.error(request, "У вас нет прав для просмотра продуктов. Пройдите авторизацию.")
    #         return HttpResponseRedirect(reverse('user:login'))
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):  # переопределяем метод get_context_data для передачи дополнительных данных в контекст
        context = super().get_context_data(
            object_list=None, **kwargs
        )  # получаем контекст из родительского класса ListView
        context["title"] = "Магазинчик"  # добавляем в контекст новый ключ title со значением 'Магазинчик'
        context["text"] = (
            "Отличный магазинчик"  # добавляем в контекст новый ключ text со значением 'Отличный магазинчик'
        )
        for product in context["object_list"]:  # перебираем все объекты из контекста
            # product.versions = Version.objects.filter(product=product).order_by('version_number')
            product.all_versions = Version.objects.filter(product=product).order_by("version_number")
            # добавляем в объект продукта все версии

        return context  # возвращаем контекст


class ContactsTemplateView(FormView):
    """Класс для отображения страницы контактов и отправки формы"""

    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Отправка формы"""
        if form.is_valid():  # проверяем валидность формы
            print(form.cleaned_data)  # выводим в консоль данные формы
        return super().form_valid(form)  # вызываем метод form_valid родительского класса

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляем заголовок на страницу контактов"""
        context = super().get_context_data(object_list=None, **kwargs)  # получаем контекст из родительского класса
        context["title"] = "Контакты"  # добавляем в контекст новый ключ title со значением 'Контакты'
        return context  # возвращаем контекст


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, IsPublishedQuerysetMixin, DetailView):
    """Информация о продукте"""

    model = Product
    template_name = "catalog/product_info.html"
    permission_required = "catalog.view_product"

    @method_decorator(cache_page(60 * 15)) # кэширование страницы на 15 минут
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCreateView(
    ProductMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView
):  # создаем класс BlogCreateView, который наследуется от CreateView
    """Класс для создания нового продукта"""

    permission_required = "catalog.add_product"
    success_url = reverse_lazy("catalog:home")  # указываем URL, на который будет перенаправлен пользователь после


class ProductUpdateView(
    ProductMixin, LoginRequiredMixin, PermissionRequiredMixin, IsPublishedQuerysetMixin, UpdateView
):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    """Класс для изменения продукта"""

    permission_required = "catalog.change_product"
    form_class = UpdateProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse("catalog:product_info", kwargs={"pk": self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен


# class ProductDeleteView(
#     LoginRequiredMixin,
#     PermissionRequiredMixin,
#     IsPublishedQuerysetMixin,
#     DeleteView
# ):
#     """ Класс для удаления продукта"""
#     model = Product
#     permission_required = "catalog.delete_product"
#     success_url = reverse_lazy("catalog:home")
