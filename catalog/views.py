from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, FormView, CreateView, UpdateView

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):  # переопределяем метод get_context_data для передачи дополнительных данных в контекст
        context = super().get_context_data(object_list=None, **kwargs)  # получаем контекст из родительского класса ListView
        context["title"] = 'Магазинчик'  # добавляем в контекст новый ключ title со значением 'Магазинчик'
        context["text"] = 'Отличный магазинчик'  # добавляем в контекст новый ключ text со значением 'Отличный магазинчик'

        context["versions"] = Version.objects.filter(is_active=True).all()

        # for product in context["object_list"]:
        #     product.version = Version.objects.filter(is_active=True, product=product).first()
        return context


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


class ProductMixin:
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"


class ProductCreateView(ProductMixin,
                        CreateView):  # создаем класс BlogCreateView, который наследуется от CreateView
    success_url = reverse_lazy("catalog:home")  # указываем URL, на который будет перенаправлен пользователь после


class ProductUpdateView(ProductMixin,
                        UpdateView):  # создаем класс BlogUpdateView, который наследуется от UpdateView
    def get_success_url(self):  # переопределяем метод get_success_url
        return reverse('catalog:product_info', kwargs={'pk': self.get_object().pk})
        # возвращаем URL, на который будет перенаправлен
