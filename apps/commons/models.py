import uuid

from django.db import models


class TimeStampAbstractModel(models.Model):
    """
    Abstract model to add two fields to inherited ones:
    created_at - when given object (row) was created
    updated_at - when given object (row) was updated
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UUIDAbstractModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
