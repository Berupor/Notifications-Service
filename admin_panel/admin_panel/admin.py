from .models import User, Template
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    search_fields = ("id", "email")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "event_name")
    search_fields = ("id", "event_name")
