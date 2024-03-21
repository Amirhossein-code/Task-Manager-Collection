from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from app.models import Customer


class CustomerInline(admin.StackedInline):
    model = Customer
    extra = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [CustomerInline]

    list_display = ["email", "is_staff", "is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_active"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
