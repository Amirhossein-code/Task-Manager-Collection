from django.contrib import admin
from ..models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "individual",
    )

    search_fields = ("title",)

    list_filter = ("individual",)

    fields = (
        "title",
        "individual",
    )
