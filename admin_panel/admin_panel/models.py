import uuid

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
    premium = models.BooleanField(default=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name


class Notification(TimeStampedMixin):
    name = models.CharField(max_length=255)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return self.name


class Template(UUIDMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    html = models.TextField(null=False)
    notification_name = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = "template"

    def __str__(self):
        return self.name


class Schedule(UUIDMixin, TimeStampedMixin):
    crontab = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "schedule"

    def __str__(self):
        return self.name