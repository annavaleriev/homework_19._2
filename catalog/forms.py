from django import forms
from django.forms import ModelForm

from catalog.models import Product


class ContactForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "category", "image", "price"]
