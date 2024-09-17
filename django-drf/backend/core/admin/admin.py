from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models import user
from individual.models import Individual


class IndividualInline(admin.StackedInline):
    model = Individual
    extra = 1


@admin.register(user)
class CustomUserAdmin(UserAdmin):
    inlines = [IndividualInline]

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
