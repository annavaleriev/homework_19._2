from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, FormView

from catalog.forms import ContactForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["title"] = 'Магазинчик'
        context["text"] = 'Отличный магазинчик'
        return context


# def product_info(request, pk):
#     """ Отображение информации о продукте """
#     product = Product.objects.get(pk=pk) # Получение объекта из БД
#     context = { # Контекст шаблона
#         'title': "Описание продукта", # Заголовок страницы
#         'product': product # Объект продукта
#     }
#     return render(request, 'catalog/product_info.html', context) # Вывод шаблона с контекстом


class ContactsTemplateView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        if form.is_valid():
            print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["title"] = 'Контакты'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_info.html"
