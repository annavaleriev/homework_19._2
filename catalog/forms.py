from django import forms
from django.forms import ModelForm

from catalog.models import Product


class ContactForm(forms.Form):
    "Класс формы для обратной связи"
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
    "Класс формы для создания и редактирования продукта"

    class Meta:
        model = Product
        fields = ["title", "description", "category", "image", "price"]

    def clean_title(self):
        "Метод проверяет наличие запрещенных слов в названии"
        title = self.cleaned_data["title"]
        stop_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in stop_words:
            if word in title.lower():
                raise forms.ValidationError(f"Использовать '{word}' в названии нельзя")
        return title

    def clean_description(self):
        "Метод проверяет наличие запрещенных слов в описании"
        description = self.cleaned_data["description"]
        stop_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in stop_words:
            if word in description.lower():
                raise forms.ValidationError(f"Использовать '{word}' в описании нельзя")
        return description
