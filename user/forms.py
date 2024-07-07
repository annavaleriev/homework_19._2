from django.contrib.auth.forms import BaseUserCreationForm

from catalog.forms import StyleFormMixin
from user.models import User


class RegisterForm(StyleFormMixin, BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
