from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()
