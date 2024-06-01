from django import forms
from django.forms import ModelForm, BooleanField

from catalog.models import Product


class ContactForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()


# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.field.items():
#             if isinstance(field, BooleanField):
#                 field.widget.attrs["class"] = "form-check-input"
#             else:
#                 field.widget.attrs["class"] = "form-control"
#   тут ошибка, нет поля field


class ProductForm(ModelForm):  # потом вставить StyleFormMixin
    class Meta:
        model = Product
        fields = ["title", "description", "category", "image", "price"]
