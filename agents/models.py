from django.db import models

from core.models import (
    BaseModel,
    Status
)

from core.utils import (
    generate_reference
)

class Agent(BaseModel):
    name    = models.CharField(max_length=255)
    version = models.FloatField(default=0.1)

    def __str__(self):
        return self.name

class Chat(BaseModel):
    user       = models.TextField()

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(Chat, 15)
        super().save(*args, **kwargs)

class ChatMessage(BaseModel):
    agent   = models.ForeignKey('agents.Agent', on_delete=models.CASCADE, blank=True, null=True)
    user    = models.TextField(blank=True, null=True)
    chat    = models.ForeignKey('agents.Chat', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(ChatMessage, 20)
        super().save(*args, **kwargs)

    def get_messaages(self):
        return self.objects.filter(chat=self.chat).order_by('-created_at')

    def get_last_message(self):
        return self.get_messaages().first()
