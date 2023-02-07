from django.contrib import admin
from .models import User, Notification, Template, Schedule


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'premium')
    search_fields = ('email',)
    list_filter = ('premium',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'priority')
    list_filter = ('priority', 'created')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('crontab', 'name')
    list_filter = ('crontab',)
