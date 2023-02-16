import requests
from config.project_config import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .models import (Characteristic, Notification, Schedule, Template, User,
                     UserCharacteristic, UserNotification)


class UserCharacteristicInline(admin.TabularInline):
    model = UserCharacteristic
    extra = 1
    autocomplete_fields = ("characteristic",)


class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    extra = 1
    readonly_fields = ("sent",)
    autocomplete_fields = ("notification",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserCharacteristicInline, UserNotificationInline)
    list_display = ("name", "email", "id")
    search_fields = ("name", "email")
    ordering = ("name",)
    list_filter = ("characteristic__name",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        user = form.instance

        for formset in formsets:
            if formset.model == UserNotification:
                for obj in formset.new_objects:

                    user_notification = UserNotification.objects.get(
                        user=user.id, notification=obj.notification
                    )

                    if obj.notification.schedule.name == "Now":
                        url = f"http://{settings.fastapi.host}:{settings.fastapi.port}/api/v1/notification/email/{user.id}"

                        data = {
                            "notification_name": obj.notification.name,
                            "priority": obj.notification.priority,
                            "data": obj.notification.data,
                        }
                        try:
                            response = requests.post(url, json=data)
                            if response.status_code == 200:
                                messages.success(
                                    request,
                                    f"Notification '{obj.notification.name}' was sent successfully to user '{user.name}'.",
                                )
                                user_notification.sent = True
                                user_notification.save()
                            else:
                                messages.warning(
                                    request,
                                    f"Failed to send notification '{obj.notification.name}' to user '{user.name}'.",
                                )
                        except requests.exceptions.RequestException as e:
                            messages.error(
                                request,
                                f"An error occurred while sending notification '{obj.notification.name}' to user '{user.name}': {str(e)}",
                            )
                        return HttpResponseRedirect(request.path_info)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    search_fields = ("characteristic",)
    list_display = ("name",)
    ordering = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "schedule",
        "priority",
    )
    search_fields = ("name", "schedule__name")
    ordering = ("priority",)
    list_filter = ("schedule", "priority")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "crontab", "name")
    search_fields = ("name",)
    ordering = ("created",)


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user", "notification")
    list_display = ("user", "notification")
    list_filter = ("user", "notification")
