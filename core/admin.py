from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminAuth(UserAdmin):
    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_active",
        "is_superuser",
        "is_staff",
    )
    search_fields = ("email", "username")
    readonly_fields = ("id", "date_joined", "last_login", "device_id", "last_ip", "ua")
    filter_horizontal = ()
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = ()


admin.site.register(User, UserAdminAuth)
