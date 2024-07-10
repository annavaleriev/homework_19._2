import random
import secrets

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from config.settings import EMAIL_HOST_USER
from user.forms import ChangeUserForm, RegisterForm
from user.models import User


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        messages.info(self.request, message="Для авторизации подтвердите почту и потом залогиньтесь")
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("user:login"))


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = "user/password_reset.html"  # нет еще этого шаблона
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.form_invalid(form)

        new_password = "".join(random.choices("abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=12))

        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.save()

        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return super().form_valid(form)


class UserChangeView(UpdateView):
    model = User
    form_class = ChangeUserForm
    success_url = reverse_lazy("catalog:home")
    template_name = "user/change.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.pk == kwargs.get("pk"):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
