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

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name


class Template(UUIDMixin):
    id = models.AutoField(primary_key=True)
    html = models.TextField(null=False)
    event_name = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        indexes = [models.Index(fields=["event_name"])]
        db_table = "template"

    def __str__(self):
        return self.event_name


class Schedule(UUIDMixin):
    crontab = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "schedule"


class Event(TimeStampedMixin):
    """
    Модель не окончательная и требует доработки.
    """

    id_schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, null=True, related_name="events"
    )
    id_user = models.UUIDField(null=False)
    email = models.EmailField(max_length=255, null=True)
    message = models.TextField(null=True)
    event = models.CharField(max_length=255, null=False)
    priority = models.IntegerField(null=True)

    class Meta:
        db_table = "event"

    def __str__(self):
        return self.event
