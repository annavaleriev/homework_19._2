from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm

from catalog.forms import StyleFormMixin
from user.models import User


class RegisterForm(StyleFormMixin, BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class ChangeUserForm(StyleFormMixin, UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("phone", "avatar", "country", "first_name", "last_name")
