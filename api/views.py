from pickle import NONE
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


from agents.models import (
    Agent,
    Chat,
    ChatMessageType,
    ChatMessage
)

from core.ai_fitness_coach import (
    AIFitnessCoach
)

from phonenumbers import geocoder, parse
from datetime import datetime
import requests
import json


ai_fitness_coach = AIFitnessCoach(api_key=settings.GEMINI_API_KEY)

class AuthMixin:
    def dispatch(self, request, *args, **kwargs):

        context        = {}
        request_origin = request.META.get('HTTP_REFERER')
        authorization  = request.headers.get('Authorization', '')
        authorization  = authorization.replace('Bearer ', '')
        # api_key        = APIKey.objects.filter(key=authorization, status__reference='ACTIVE').first()

        # if api_key is None:
            # context['code']    = 400
            # context['message'] = "Unauthorized"
            # return JsonResponse(context)

        # self.api_key          = api_key
        return super().dispatch(request, *args, **kwargs)

class ChatsView(AuthMixin, APIView):
    endpoint = '/api/chats'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.GET.get('user_id', None)

        if not user_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        chats       = Chat.objects.filter(user=user_id)
        chats_data  = []

        for chat in chats:
            last_message = chat.get_last_message()
            chats_data.append({
                'reference'     : chat.reference,
                'created_at'    : chat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at'    : chat.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deleted'       : chat.deleted,
                'last_message'  : {
                    'id'        : last_message.reference,
                    'agent'     : {'id': last_message.agent.reference}   if last_message.agent is not None else None,
                    'user'      : {'id': last_message.user}              if last_message.user is not None else None,
                    'direction' : 'recieved' if last_message.agent is not None else 'sent',
                    'message'   : last_message.message,
                    'created_at': last_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'deleted'   : last_message.deleted,
                },
            })

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': user_id},
            'chats'  : chats_data
        }
        return JsonResponse(context)

class ChatView(AuthMixin, APIView):
    endpoint = '/api/chat'
    def post(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        post_data       = json.loads(request.body.decode())

        user_id         = post_data.get('user_id', None)
        chat_id         = post_data.get('chat_id', None)
        user_message    = post_data.get('message', None)

        if user_message is None or user_id is None:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        chat = Chat.objects.filter(reference=chat_id, user=user_id).first()

        if chat is None:
            chat = Chat.objects.create(user=user_id)

        elif chat.get_last_message() is not None and chat.get_last_message().agent is None:
            context['code']    = 400
            context['message'] = "Pending agent response"
            return JsonResponse(context)

        message_type = ChatMessageType.objects.filter(reference='direct_question').first()
        user_message = ChatMessage.objects.create(message_type=message_type, chat=chat, user=user_id, message=user_message)

        chat_agent      =  Agent.objects.filter(reference='chat_agent').last()

        new_message     = ai_fitness_coach.process_user_message(user_message.message)

        message_type    = ChatMessageType.objects.filter(reference='direct_answer').first()
        agent_message   = ChatMessage.objects.create(message_type=message_type, chat=chat, agent=chat_agent, message=new_message)

        context['code'] = 200
        context['data'] = {
            'chat'   : {
                'id' : chat.reference,
            },
            'user_message'  : {
                'id'        : user_message.reference,
                'message'   : user_message.message,
                'agent'     : None,
                'user'      : {'id': user_message.user},
                'direction' : 'sent',
                'created_at': user_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user_message.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deleted'   : user_message.deleted,
            },
            'agent_message' : {
                'id'        : agent_message.reference,
                'message'   : agent_message.message,
                'agent'     : {'id': agent_message.agent.reference},
                'user'      : None,
                'direction' : 'recieved',
                'created_at': agent_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': agent_message.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deleted'   : agent_message.deleted,
            }
        }
        return JsonResponse(context)

class ChatHistoryView(AuthMixin, APIView):
    endpoint = '/api/chat-history'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.GET.get('user_id', None)
        chat_id         = request.GET.get('chat_id', None)

        if not chat_id or not user_id:
            context['code']    = 400
            context['message'] = "Bad Request"
            return JsonResponse(context)

        chat = Chat.objects.filter(reference=chat_id, user=user_id).first()

        if chat is None:
            context['code']    = 400
            context['message'] = "Chat not found"
            return JsonResponse(context)

        messages_data = []
        for message in chat.get_messages():
            messages_data.append({
                'id'        : message.reference,
                'agent'     : {'id': message.agent.reference}   if message.agent is not None else None,
                'user'      : {'id': message.user}              if message.user is not None else None,
                'direction' : 'recieved' if message.agent is not None else 'sent',
                'message'   : message.message,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': message.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deleted'   : message.deleted,
            })

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': chat.user},
            'chat'   : {'id': chat.reference},
            'messages': messages_data
        }
        return JsonResponse(context)
