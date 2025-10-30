from django.db import models

from core.models import (
    BaseModel,
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

    def get_messaages(self):
        return ChatMessage.objects.filter(chat=self).order_by('-created_at')

    def get_messages_ai_formatted(self):
        data = []
        for message in self.get_messaages():
            data.append({
                'sent_by_ai_agent'  : message.agent is not None,
                'sent_by_user'      : message.user is not None,
                'direction'         : 'sent' if message.user is not None else 'received',
                'message'           : message.message
            })
        return data

    def get_last_message(self):
        return self.get_messaages().first()

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(Chat, 15)
        super().save(*args, **kwargs)

class ChatMessageType(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ChatMessage(BaseModel):
    message_type = models.ForeignKey('agents.ChatMessageType', on_delete=models.CASCADE, blank=True, null=True)
    agent        = models.ForeignKey('agents.Agent', on_delete=models.CASCADE, blank=True, null=True)
    user         = models.TextField(blank=True, null=True)
    chat         = models.ForeignKey('agents.Chat', on_delete=models.CASCADE)
    message      = models.TextField()

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(ChatMessage, 20)
        super().save(*args, **kwargs)
