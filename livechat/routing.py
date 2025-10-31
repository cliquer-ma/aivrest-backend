from django.urls import path

from livechat.consumers import (
    LiveChatConsumer
)

websocket_urlpatterns = [
    path("ws/live-chat/<str:reference>/",            LiveChatConsumer.as_asgi()),
]
