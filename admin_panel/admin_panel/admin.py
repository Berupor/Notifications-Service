from django.contrib import admin
from .models import User, Characteristic, UserCharacteristic, Notification, Template, Schedule, UserNotification


class UserCharacteristicInline(admin.TabularInline):
    model = UserCharacteristic
    extra = 1
    autocomplete_fields = ("characteristic",)


class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    extra = 1
    autocomplete_fields = ("notification",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserCharacteristicInline, UserNotificationInline)
    list_display = ('name', 'email', "id")
    search_fields = ('name', 'email')
    ordering = ('name',)
    list_filter = ('characteristic__name',)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    search_fields = ("characteristic", )
    list_display = ('name', )
    ordering = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'priority',)
    search_fields = ('name', 'schedule__name')
    ordering = ('priority',)
    list_filter = ("schedule", "priority")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'crontab', 'name')
    search_fields = ('name',)
    ordering = ('created',)
