from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    return render(
        request,
        "catalog/home.html",
        context={
            'title': 'Магазинчик',
            'text': 'Отличный магазинчик',
            'products': product_list
        }
    )


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#     return render(
#         request,
#         "catalog/contacts.html",
#         context={
#             'title': 'Контакты'
#         }
#     )
#

# def product_info(request, pk):
#     """ Отображение информации о продукте """
#     product = Product.objects.get(pk=pk) # Получение объекта из БД
#     context = { # Контекст шаблона
#         'title': "Описание продукта", # Заголовок страницы
#         'product': product # Объект продукта
#     }
#     return render(request, 'catalog/product_info.html', context) # Вывод шаблона с контекстом


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
        return render(
            request,
            "catalog/contacts.html",
            context={
                'title': 'Контакты'
            }
        )


class ProductDetailView(DetailView):
    model = Product
