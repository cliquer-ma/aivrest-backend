from django.db import models

from core.models import (
    BaseModel,
)

class CompetitionStatus(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class VideoSubmissionStatus(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class Competition(BaseModel):
    challenge_type      = models.CharField(max_length=255)
    title               = models.CharField(max_length=255)
    description         = models.TextField(default="")
    difficulty          = models.CharField(max_length=255)
    duration_days       = models.IntegerField(default=0)
    image_url           = models.TextField(default="")
    instructions        = models.TextField(default="")
    max_participants    = models.IntegerField(default=0)
    participants_count  = models.IntegerField(default=0)
    prize               = models.TextField(default="")
    rules               = models.JSONField(default=list)
    status              = models.ForeignKey("competitions.CompetitionStatus", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(Competition, 10)
        super().save(*args, **kwargs)

class VideoSubmission(BaseModel):
    user            = models.TextField(blank=True, null=True)
    competition     = models.ForeignKey("competitions.Competition", on_delete=models.CASCADE)
    comment         = models.TextField(blank=True, null=True)
    status          = models.ForeignKey("competitions.VideoSubmissionStatus", on_delete=models.CASCADE)
    content_type    = models.CharField(max_length=255)
    file_size       = models.CharField(max_length=255)
    video_filename  = models.TextField()
    video_url       = models.TextField()

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(VideoSubmission, 20)
        super().save(*args, **kwargs)
