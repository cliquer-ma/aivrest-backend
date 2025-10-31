from django.db import models

from core.models import (
    BaseModel
)


class LiveChatRoom(BaseModel):
    users = models.JSONField(default=list)

    def __str__(self):
        return self.reference
    
    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(LiveChatRoom, 10)
        super().save(*args, **kwargs)

class LiveChatMessageType(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class LiveChatMessage(BaseModel):
    room         = models.ForeignKey("livechat.LiveChatRoom", on_delete=models.CASCADE)
    message_type = models.ForeignKey("livechat.LiveChatMessageType", on_delete=models.CASCADE)
    from_user    = models.TextField(default="")
    to_user      = models.TextField(default="")
    content      = models.TextField(default="")

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(LiveChatMessage, 10)
        super().save(*args, **kwargs)
