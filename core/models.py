from django.db import models

from core.utils import (
    generate_reference
)

class BaseModel(models.Model):
    reference  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    deleted    = models.BooleanField(default=False)

    def __str__(self):
        self.reference

    class Meta: 
        abstract = True

class AppSettings(BaseModel):
    version   = models.FloatField(default=0.1)

    def __str__(self):
        return self.reference


class Status(BaseModel):
    label = models.JSONField(default=dict)

    def __str__(self):
        return self.label
