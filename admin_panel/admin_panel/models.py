import uuid

from django.contrib.gis.db import models


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


class Template(UUIDMixin):
    id = models.AutoField(primary_key=True)
    html = models.TextField(null=False)
    event_name = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        indexes = [
            models.Index(fields=['event_name'])
        ]
