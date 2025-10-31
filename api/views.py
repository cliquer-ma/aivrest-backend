from pickle import NONE
import base64
import os
import uuid
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.db.models import OuterRef, Subquery
import cloudinary
import cloudinary.uploader
import cloudinary.api

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

from programs.models import (
    ProgramType,
    Program,
)

from posts.models import (
    Post,
    PostLike,
    PostComment
)

from livechat.models import (
    LiveChatRoom,
    LiveChatMessageType,
    LiveChatMessage
)

from core.ai_fitness_coach import (
    AIFitnessCoach
)

import cloudinary
import cloudinary.uploader
import cloudinary.api

from phonenumbers import geocoder, parse
from datetime import datetime
import requests
import json

import base64
import os
import uuid

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
        min_date_str    = request.GET.get('min_date', None)

        min_date        = None

        if not user_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)


        chats       = Chat.objects.filter(user=user_id)
        chats_data  = []

        if min_date is not None:

            try:
                min_date = datetime.strptime(min_date_str, '%Y-%m-%d')
            except:
                context['code']    = 400
                context['message'] = "Invalid Date Format"
                return JsonResponse(context)


            chats = chats.filter(created_at__gte=min_date)

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
                } if last_message is not None else {},
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

        user_id         = request.POST.get('user_id', None)
        chat_id         = request.POST.get('chat_id', None)
        user_message    = request.POST.get('message', None)

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

        chat_history    = chat.get_messages_ai_formatted()

        message_type    = ChatMessageType.objects.filter(reference='direct_question').first()
        user_message    = ChatMessage.objects.create(message_type=message_type, chat=chat, user=user_id, message=user_message)

        chat_agent      = Agent.objects.filter(reference='chat_agent').last()
        new_message     = ai_fitness_coach.process_user_message(user_message.message, chat_history)

        message_type    = ChatMessageType.objects.filter(reference='direct_answer').first()
        agent_message   = ChatMessage.objects.create(message_type=message_type, chat=chat, agent=chat_agent, message=new_message)

        context['code'] = 200
        context['data'] = {
            'chat'   : {'id' : chat.reference},
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

class ProgramsTypesView(AuthMixin, APIView):
    endpoint = '/api/programs-types'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        program_types   = ProgramType.objects.all()
        program_types_data = []

        for program_type in program_types:
            program_types_data.append({
                'id'            : program_type.reference,
                'label'         : program_type.label,
            })

        context['code'] = 200
        context['data'] = {
            'program_types': program_types_data
        }
        return JsonResponse(context)

class ProgramsView(AuthMixin, APIView):
    endpoint = '/api/programs'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.GET.get('user_id', None)

        if not user_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        programs        = Program.objects.filter(user=user_id)
        programs_data   = []

        for program in programs:
            programs_data.append({
                'id'            : program.reference,
                'program_type'  : {'id': program.program_type.reference},
                'title'         : program.title,
                'content'       : program.content,
                'duration_days' : program.duration_days,
                'level'         : program.level,
            })

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': user_id},
            'programs': programs_data
        }
        return JsonResponse(context)

class ProgramView(AuthMixin, APIView):
    endpoint = '/api/program'
    def post(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.POST.get('user_id', None)
        program_id      = request.POST.get('program_id', None)
        
        if not user_id or not program_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)
            
        program = Program.objects.filter(reference=program_id, user=user_id).first()

        if program is None:
            context['code']    = 400
            context['message'] = "Program not found"
            return JsonResponse(context)

        program_data = {
            'id'            : program.reference,
            'program_type'  : {'id': program.program_type.reference},
            'title'         : program.title,
            'content'       : program.content,
            'duration_days' : program.duration_days,
            'level'         : program.level,
        }

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': user_id},
            'program': program_data
        }
        return JsonResponse(context)


class PostsView(AuthMixin, APIView):
    endpoint = '/api/posts'
    per_page = 30
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.GET.get('user_id', None)

        posts           = Post.objects.filter(deleted=False).order_by('-created_at')

        if user_id is not None:
            posts = posts.filter(user=user_id)

        posts_data      = []

        for post in posts:
            posts_data.append({
                'id'            : post.reference,
                'user'          : {'id': post.user},
                'content'       : post.content,
                'attachements'  : post.attachements,
                'liked'         : PostLike.objects.filter(post=post, user=user_id).exists(),
                'created_at'    : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at'    : post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': user_id},
            'posts'  : posts_data
        }
        return JsonResponse(context)
    
class PostView(AuthMixin, APIView):
    endpoint = '/api/post'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        post_id         = request.GET.get('post_id', None)
        user_id         = request.GET.get('user_id', None)

        if not post_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)
            
        post = Post.objects.filter(reference=post_id).first()

        if post is None:
            context['code']    = 400
            context['message'] = "Post not found"
            return JsonResponse(context)
            
        post_data = {
            'id'            : post.reference,
            'user'          : {'id': post.user},
            'content'       : post.content,
            'attachements'  : post.attachements,
            'liked'         : PostLike.objects.filter(post=post, user=user_id).exists(),
            'created_at'    : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at'    : post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        context['code'] = 200
        context['data'] = {
            'post'          : post_data
        }
        return JsonResponse(context)
    
class PostLikesView(AuthMixin, APIView):
    endpoint = '/api/post-likes'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        post_id         = request.GET.get('post_id', None)

        if not post_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)
            
        post = Post.objects.filter(reference=post_id).first()

        if post is None:
            context['code']    = 400
            context['message'] = "Post not found"
            return JsonResponse(context)
            
        likes      = PostLike.objects.filter(post=post)
        likes_data = []

        for post_like in likes:
            likes_data.append({
                'user'          : {'id': post_like.user},
                'created_at'    : post_like.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at'    : post_like.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        context['code'] = 200
        context['data'] = {
            'post'          : {'id': post.reference},
            'likes'         : likes_data
        }
        return JsonResponse(context)

class PostCommentsView(AuthMixin, APIView):
    endpoint = '/api/post-comments'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        post_id         = request.GET.get('post_id', None)

        if not post_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)
        
        post = Post.objects.filter(reference=post_id).first()

        if post is None:
            context['code']    = 400
            context['message'] = "Post not found"
            return JsonResponse(context)
            
        comments      = PostComment.objects.filter(post=post)
        comments_data = []

        for post_comment in comments:
            comments_data.append({
                'user'          : {'id': post_comment.user},
                'content'       : post_comment.content,
                'created_at'    : post_comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at'    : post_comment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        context['code'] = 200
        context['data'] = {
            'post'          : {'id': post.reference},
            'comments'      : comments_data
        }
        return JsonResponse(context)

class TogglePostLikeView(AuthMixin, APIView):
    endpoint = '/api/like-post'
    def post(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.POST.get('user_id', None)
        post_id         = request.POST.get('post_id', None)

        if not user_id or not post_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        post = Post.objects.filter(reference=post_id).first()

        if post is None:
            context['code']    = 400
            context['message'] = "Post not found"
            return JsonResponse(context)

        like = PostLike.objects.filter(post=post, user=user_id).first()

        if like is None:
            like = PostLike.objects.create(post=post, user=user_id)
        else:
            like.delete()
        
        context['code'] = 200
        context['data'] = {
            'post'          : {'id': post.reference},
            'liked'         : like is not None
        }
        return JsonResponse(context)

class CommentPostView(AuthMixin, APIView):
    endpoint = '/api/comment-post'
    def post(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.POST.get('user_id', None)
        post_id         = request.POST.get('post_id', None)
        content         = request.POST.get('content', None)

        if not user_id or not post_id or not content:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        post = Post.objects.filter(reference=post_id).first()

        if post is None:
            context['code']    = 400
            context['message'] = "Post not found"
            return JsonResponse(context)

        comment = PostComment.objects.create(post=post, user=user_id, content=content)

        context['code'] = 200
        context['data'] = {
            'post'          : {'id': post.reference},
            'comment'       : {'id': comment.reference}
        }
        return JsonResponse(context)

class CreatePostView(AuthMixin, APIView):
    endpoint = '/api/create-post'
    def post(self, request, format=None):
        context = {}

        user_id = request.POST.get('user_id', None)
        content = request.POST.get('content', None)
        base64_attachments = request.POST.getlist('attachments[]')  # Expecting a list of base64 strings

        if not user_id or not content:
            context['code'] = 400
            context['message'] = "User ID and content are required"
            return JsonResponse(context, status=400)

        # Create the post with attachment URLs as a comma-separated string
        post = Post.objects.create(
            user=user_id,
            content=content,
            attachements = attachment_urls
        )

        context['code'] = 200
        context['data'] = {
            'post': {
                'id': post.reference,
                'attachments': attachment_urls
            }
        }
        return JsonResponse(context)
        return JsonResponse(context)


class RoomsView(AuthMixin, APIView):
    endpoint = '/api/rooms'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.GET.get('user_id', None)

        if not user_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        # Get the latest message for each room
        latest_messages = LiveChatMessage.objects.filter(
            room=OuterRef('pk')
        ).order_by('-created_at')
        
        # Get rooms with their latest message
        rooms = LiveChatRoom.objects.filter(
            users__contains=[user_id]
        ).annotate(
            last_message_content=Subquery(latest_messages.values('content')[:1]),
            last_message_created=Subquery(latest_messages.values('created_at')[:1]),
            last_message_type=Subquery(latest_messages.values('message_type__reference')[:1]),
            last_message_sender=Subquery(latest_messages.values('from_user')[:1])
        )

        rooms_data = []
        for room in rooms:
            room_data = {
                'id': room.reference,
                'users': room.users,
            }
            
            # Add last message data if exists
            if room.last_message_content is not None:
                room_data['last_message'] = {
                    'content': room.last_message_content,
                    'created_at': room.last_message_created.isoformat() if room.last_message_created else None,
                    'message_type': room.last_message_type,
                    'from_user': room.last_message_sender
                }
            
            rooms_data.append(room_data)

        context['code'] = 200
        context['data'] = {
            'user'   : {'id': user_id},
            'rooms'  : rooms_data
        }
        return JsonResponse(context)

class CreateRoomView(AuthMixin, APIView):
    endpoint = '/api/create-room'
    def post(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        user_id         = request.POST.get('user_id', None)
        user_id2        = request.POST.get('user_id2', None)

        if not user_id or not user_id2:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        room = LiveChatRoom.objects.create(users=[user_id, user_id2])

        context['code'] = 200
        context['data'] = {
            'room'          : {'id': room.reference},
            'users'         : room.users,
        }
        return JsonResponse(context)

class RoomView(AuthMixin, APIView):
    endpoint = '/api/room'
    def get(self, request, format=None):
        context          = {}
        # api_key          = self.api_key

        room_id         = request.GET.get('room_id', None)

        if not room_id:
            context['code']    = 400
            context['message'] = "Invalid parameters"
            return JsonResponse(context)

        room = LiveChatRoom.objects.filter(reference=room_id).first()

        if room is None:
            context['code']    = 400
            context['message'] = "Room not found"
            return JsonResponse(context)

        messages        = LiveChatMessage.objects.filter(room=room).order_by('-created_at')
        messages_data   = []

        for message in messages:
            messages_data.append({
                'id'            : message.reference,
                'message_type'  : {
                    'id'        : message.message_type.reference,
                    'label'     : message.message_type.label,
                },
                'from_user'     : message.from_user,
                'to_user'       : message.to_user,
                'content'       : message.content,
            })

        context['code'] = 200
        context['data'] = {
            'room'          : {'id': room.reference},
            'messages'      : messages_data
        }
        return JsonResponse(context)
