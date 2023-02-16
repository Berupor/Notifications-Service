import uuid

import requests  # type: ignore
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(UUIDMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    characteristic = models.ManyToManyField(
        "Characteristic", through="UserCharacteristic"
    )
    notification = models.ManyToManyField("Notification", through="UserNotification")

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "characteristic"

    def __str__(self):
        return self.name


class Notification(TimeStampedMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    schedule = models.ForeignKey("Schedule", on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField()
    template = models.ForeignKey("Template", on_delete=models.CASCADE)
    data = models.JSONField()

    class Meta:
        db_table = "notification"

    def __str__(self):
        return self.name


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    html = models.TextField(null=False)

    class Meta:
        db_table = "template"

    def __str__(self):
        return self.name


class Schedule(TimeStampedMixin):
    id = models.AutoField(primary_key=True)
    crontab = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "schedule"

    def __str__(self):
        return self.name


class UserCharacteristic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_characteristic"
        unique_together = ("user", "characteristic")


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    sent = models.BooleanField(default=False)

    class Meta:
        db_table = "user_notification"
        unique_together = ("user", "notification")

    def __str__(self):
        return f"{self.user.name} – {self.notification.name}"
