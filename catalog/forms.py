from django import forms
from django.forms import ModelForm, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    """Класс для добавления стилей к формам"""

    def __init__(self, *args, **kwargs):  # переопределяем метод __init__
        super().__init__(*args, **kwargs)  # вызываем родительский метод __init__
        for field_name, field in self.fields.items():  # перебираем все поля формы
            if isinstance(field, BooleanField):  # если поле является BooleanField
                field.widget.attrs["class"] = "form-check-input"  # добавляем класс form-check-input
            else:
                field.widget.attrs["class"] = "form-control"  # добавляем класс form-control


class ContactForm(StyleFormMixin, forms.Form):
    """Класс формы для обратной связи"""
    name = forms.CharField()  # добавляем поле name
    phone = forms.CharField()  # добавляем поле phone
    message = forms.CharField()  # добавляем поле message


class ProductForm(StyleFormMixin, ModelForm):  # потом вставить StyleFormMixin
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product
        fields = ["title", "description", "category", "image", "price"]

    # def save(self, commit=True):
    #     super().save()

    @staticmethod
    def check_wrong_words(field_value):
        """Метод проверяет наличие запрещенных слов в поле"""
        stop_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in stop_words:
            if word in field_value.lower():  # если слово из списка stop_words есть в поле
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


class VersionForm(StyleFormMixin, ModelForm):
    """ Форма для создания и редактирования версии продукта"""

    class Meta:
        model = Version
        fields = ["version_name", "version_number", "is_active", "product"]


# VersionFormSet = forms.inlineformset_factory(Product, Version, form=VersionForm, extra=1)
# создаем формсет для того, чтобы  можно было добавлять несколько версий продукта
