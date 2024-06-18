from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "country")
    search_fields = ("email", "phone")
    ordering = ("email",)
