from django.contrib import admin
from ..models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_time",
        "finish_time",
        "priority",
        "status",
        "category",
        "individual",
        "created_at",
        "last_updated",
    )

    search_fields = (
        "title",
        "category__title",
    )

    # Filters available on the sidebar
    list_filter = (
        "priority",
        "status",
        "category",
        "individual",
    )

    # Fields to display on the form view
    fields = (
        "title",
        "description",
        "start_time",
        "finish_time",
        "priority",
        "status",
        "category",
        "individual",
    )

    readonly_fields = (
        "created_at",
        "last_updated",
    )
