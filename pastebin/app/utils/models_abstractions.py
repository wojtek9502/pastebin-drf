import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    inserted_on = models.DateTimeField(auto_now_add=timezone.now)
    updated_on = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True