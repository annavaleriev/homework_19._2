from django import forms
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductMixin:
    """Класс для добавления версий продукта"""

    model = Product
    form_class = ProductForm  # указываем форму, которая будет использоваться
    template_name = "catalog/product_form.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormSet = forms.inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            formset = VersionFormSet(self.request.POST, instance=self.object)
        else:
            formset = VersionFormSet(instance=self.object)
        context_data["formset"] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]

        with transaction.atomic():
            if form.is_valid() and formset.is_valid():
                self.object = form.save(commit=False)
                self.object.owner = self.request.user  # Привязка продукта к авторизованному пользователю
                self.object.save()
                formset.instance = self.object
                formset.save()
            else:
                for error in formset.errors:
                    messages.add_message(self.request, messages.ERROR, str(error))
                if self.object:
                    success_url = reverse("catalog:edit", kwargs={"pk": self.object.pk})
                else:
                    success_url = reverse("catalog:create")
                return HttpResponseRedirect(success_url)

        return super().form_valid(form)

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         messages.info(request, "Для добавления продукта необходимо авторизоваться.")
    #     return super().dispatch(request, *args, **kwargs)

    def check_permissions(self):
        if self.object and self.object.owner != self.request.user:
            messages.error(self.request, "У вас нет прав на редактирование этого продукта.")
            return False
        return True


class IsPublishedQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)
