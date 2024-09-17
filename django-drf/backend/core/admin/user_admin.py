from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models import User
from individual.models import Individual


class IndividualInline(admin.StackedInline):
    model = Individual
    can_delete = False
    fk_name = "user"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "email",
        "is_staff",
        "is_active",
    ]
    search_fields = [
        "phone",
    ]
    list_filter = [
        "is_staff",
        "is_active",
    ]
    readonly_fields = [
        "last_login",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ["-date_joined"]
    inlines = [IndividualInline]
