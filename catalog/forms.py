from django import forms
from django.forms import ModelForm, BooleanField

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ContactForm(StyleFormMixin, forms.Form):
    "Класс формы для обратной связи"
    name = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()


class ProductForm(StyleFormMixin, ModelForm):  # потом вставить StyleFormMixin
    "Класс формы для создания и редактирования продукта"

    class Meta:
        model = Product
        fields = ["title", "description", "category", "image", "price"]

    # def save(self, commit=True):
    #     super().save()

    @staticmethod
    def check_wrong_words(field_value):
        stop_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in stop_words:
            if word in field_value.lower():
                raise forms.ValidationError(f"Использовать '{word}' запрещено")

    def clean_title(self):
        """Метод проверяет наличие запрещенных слов в названии"""
        title = self.cleaned_data["title"]
        self.check_wrong_words(title)
        return title

    def clean_description(self):
        """Метод проверяет наличие запрещенных слов в описании"""
        description = self.cleaned_data["description"]
        self.check_wrong_words(description)
        return description
