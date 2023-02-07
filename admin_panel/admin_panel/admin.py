from django.contrib import admin

from .models import Template, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    search_fields = ("id", "email")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "event_name")
    search_fields = ("id", "event_name")
