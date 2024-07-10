"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.apps import UserConfig
from user.views import PasswordResetView, UserChangeView, UserCreateView, email_verification

app_name = UserConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    # path('logout/', include('user.urls', namespace='logout')), почему это приводит к цикличности
    # path('register/', include('user.urls', namespace='register')),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("change/<int:pk>/", UserChangeView.as_view(), name="change"),
]
