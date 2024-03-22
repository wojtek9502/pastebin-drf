import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class InsertedOnModel:
    inserted_on = models.DateTimeField(auto_now_add=timezone.now)


class UpdatedOnModel:
    updated_on = models.DateTimeField(auto_now=timezone.now)
