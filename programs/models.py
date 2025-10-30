from django.db import models

from core.models import (
    BaseModel,
)


class ProgramType(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class Program(BaseModel):
    user          = models.TextField()
    program_type  = models.ForeignKey('programs.ProgramType', on_delete=models.CASCADE)
    title         = models.CharField(max_length=255)
    content       = models.JSONField(default=list)
    duration_days = models.IntegerField(default=0)
    level         = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(Program, 10)
        super().save(*args, **kwargs)
        
