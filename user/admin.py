from django.contrib import admin
from django.contrib.auth.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "country")
    # readonly_fields = ("views", )
    search_fields = ("email", "phone")
    ordering = ("email",)


admin.site.register(User, UserAdmin)

# admin.site.register(User)
