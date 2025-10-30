from django.urls import path

from api.views import (
    ChatsView,
    ChatView,
    ChatHistoryView,
)

urlpatterns = [
    path('xenon/chats/',                ChatsView.as_view(),                name='api_chats'),
    path('xenon/send/',                 ChatView.as_view(),                 name='api_chat'),
    path('xenon/chat-history/',         ChatHistoryView.as_view(),          name='api_chat_history'),
]
