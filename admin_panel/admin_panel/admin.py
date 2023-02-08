from django.contrib import admin
from .models import User, Characteristic, UserCharacteristic, Notification, Template, Schedule


class UserCharacteristicInline(admin.TabularInline):
    model = UserCharacteristic
    autocomplete_fields = ("user",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserCharacteristicInline,)
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)
    list_filter = ('characteristic__name',)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'schedule', 'priority',)
    search_fields = ('name', 'schedule__name')
    ordering = ('priority',)
    list_filter = ("schedule", "priority")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notification')
    search_fields = ('name', 'notification__name')
    ordering = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'crontab', 'name')
    search_fields = ('name',)
    ordering = ('created',)
