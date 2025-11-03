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

import firebase_admin
from firebase_admin import credentials, firestore
import json
import tempfile
import os

# Firebase credentials
FIREBASE_PROJECT_ID = "revolusport-89884"
FIREBASE_PRIVATE_KEY_ID = "84597f40da01a6baa15e08482dfe86c70c401358"
FIREBASE_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC53whIovqeflIH
UuDk7wJ+yM1eqHtLcRlgQv4Z6wDJ9E1qxpjQT/1rKx7/ZWFYwwLSAd8CuakIZUcU
07oxYFYyKGyxHgtbluPgqsw98uBJALTntjQpEZ6BDCjnabQiV2JJb5gupDaTNGc+
RZoeXNNxzSS+p/0llqiUh9aT2W5ATSaBixIb/CkOvaHZ00w18Q81053RNfMv8UfX
S3xyHK9HwwJKBsv8t+Lq8GiIj1ag9ObD6khrkvAdeXZxgBjcwP3Zrt2pw2gVIqyB
rzNPNdO/iTvMF41P2617iF/CmiQ2JRrxBWQcnvNLh6hW/XESuN7ChuBT58+2O2Pv
vMLN23HnAgMBAAECggEAMhCRpiMEF3HV/XQE8JUyWl0S+DawcxslJykUUX3bqgoc
WjDhE2cgTuAACvHPPT3VwiRP4eeJUKIa+dCn28njncIGuNRrYcGsYqUOu3byk6dV
kv4gYZmF1KOmVuLBauiXqEkfOBzyOEdKsdrEjv4Y1BPaHGKaTKgeg1dtZEiSKk5H
zBlEFsed6wOq1uSxeUs7/TAOoeP4LrBQXImTp1uU0asHqfcVhHIRahWLhackYu+h
ACyZ4EefXt4zNObkWNWl6oNfhGch2Mv965HKulBxf8DUva1p56Xgzqg1qhKFNYEp
5xGpjkUQeFlzD9otPC/vwuPcQqWYscGtf/5jc65pOQKBgQDqOf1Cl+4Nip16nhaW
hw8kSom9FGsO5YAdYVBJ94AK8Za/dFwQAgKFNAoBfkrVX3USZQpDO6EK5SjrTp8k
yg6tfcNVPQJUFt1qI2JSq4WZnr7Jddm1vERU+vd13zWMeKEIpvgVqzsEc/O3r6N8
/JqCNOCrqFTd59LCf7sLy1nkSQKBgQDLJk6HDhHLoP2w32/83gplfEudDnXOa0+z
ias6s+CtKjJ6SoWjT4fS7vksjqBywKWo0shLP8YpbmKRkuC0CQnECJJdn/WUZY65
ZsfwViSF2w85LwDugsdvhiCeU+X2dgWdF/mWwHnxntqNcnN/cKGt/i88HBdjXiu7
b/5qmp1ErwKBgCPwkfPN7DEXu+I8r6qZPrGK3mes4mB+xpG7hN5Uo8kKGN93s0ih
hlF6Eq73+fOTmhsgddqrI6LQVt8ESVcTyfzE91v06I6Ok5rdoxCcUPupaAzxkF5a
bQG9IIttnIHZYJw7QoXQqFWelR7yTFu5RtwD0RWF1r/V+njtsH22zixBAoGAQlj0
dK9nqHWf5VBUJuXtx09c8qJyX0Q095IS1k1BJ80MR1xnYPrshTt/Lco3JMM+V3Df
8ZOWiJmAn8K0mJgLFHcoNmOztQ+mGW80BY5cx0rQIgDz8PHNaOMJbCxCgsfw9WmL
Hm0mZn9XKbMjfY+vfj/x9VPHX7C137WoBfERRAkCgYEAmW3wfuuj4dDcJnNjrUZm
7GDlwka+IxbRplbI7VTulVhu/3JP6kqKcclv13LV9vIeXs+5yCCKLppdNMDfvU8R
Q9eE45zCQCdzMKNnNhNAYDiZ2/KMR+6nlhBHuGuKuteehRCB7rnS1y1dIXt/TO2k
CjsyCF53oTDsSDWBf3ZEmVg=
-----END PRIVATE KEY-----"""
FIREBASE_CLIENT_EMAIL = "firebase-adminsdk-mekbl@revolusport-89884.iam.gserviceaccount.com"
FIREBASE_CLIENT_ID = "107131551580705863631"
FIREBASE_CLIENT_CERT_URL = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mekbl%40revolusport-89884.iam.gserviceaccount.com"

# Global database instance
db = None

def get_firebase_db():
    global db
    if db is None:
        try:
            print("🔑 Using Firebase credentials directly")
            
            firebase_credentials = {
                "type": "service_account",
                "project_id": FIREBASE_PROJECT_ID,
                "private_key_id": FIREBASE_PRIVATE_KEY_ID,
                "private_key": FIREBASE_PRIVATE_KEY,
                "client_email": FIREBASE_CLIENT_EMAIL,
                "client_id": FIREBASE_CLIENT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": FIREBASE_CLIENT_CERT_URL,
                "universe_domain": "googleapis.com"
            }
            
            print("🔍 Firebase credentials check:")
            print(f"  project_id: {'SET' if firebase_credentials['project_id'] else 'NOT SET'}")
            print(f"  private_key: {'SET' if firebase_credentials['private_key'] else 'NOT SET'}")
            print(f"  client_email: {'SET' if firebase_credentials['client_email'] else 'NOT SET'}")
            
            missing_vars = []
            if not firebase_credentials["project_id"]:
                missing_vars.append("FIREBASE_PROJECT_ID")
            if not firebase_credentials["private_key"]:
                missing_vars.append("FIREBASE_PRIVATE_KEY")
            if not firebase_credentials["client_email"]:
                missing_vars.append("FIREBASE_CLIENT_EMAIL")
                
            if missing_vars:
                print(f"⚠️  Firebase core credentials missing: {', '.join(missing_vars)}")
                db = None
                return db

            print("🔧 Initializing Firebase with credentials...")
            try:
                cred = credentials.Certificate(firebase_credentials)
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred)
                db = firestore.client()
                print(f"✅ Firebase initialized successfully")
            except Exception as firebase_error:
                print(f"⚠️ Direct credentials failed, trying temporary file approach: {firebase_error}")
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                    json.dump(firebase_credentials, temp_file, indent=2)
                    temp_file_path = temp_file.name
                
                try:
                    cred = credentials.Certificate(temp_file_path)
                    if not firebase_admin._apps:
                        firebase_admin.initialize_app(cred)
                    db = firestore.client()
                    print(f"✅ Firebase initialized successfully with temporary file")
                    os.unlink(temp_file_path)
                except Exception as temp_error:
                    print(f"❌ Temporary file approach also failed: {temp_error}")
                    try:
                        if not firebase_admin._apps:
                            firebase_admin.initialize_app()
                        db = firestore.client()
                        print(f"✅ Firebase initialized with default credentials")
                    except Exception as default_error:
                        print(f"❌ Default credentials failed: {default_error}")
                        db = None
        except Exception as e:
            print(f"❌ Firebase initialization failed: {str(e)}")
            import traceback
            print(f"❌ Full error traceback: {traceback.format_exc()}")
            db = None
    return db

def get_user_profile(user_id: str) -> dict:
    try:

        profile_ref = get_firebase_db().collection(f"users/{user_id}/userDetails").document("profile")
        profile = profile_ref.get()

        user_ref = get_firebase_db().collection("users").document(user_id)
        user_doc = user_ref.get()

        if profile.exists and user_doc.exists:
            profile_data = profile.to_dict()
            user_data = user_doc.to_dict()
        
            combined_data = {
                **profile_data,
                "full_name": user_data.get("fullname", ""),
                "hasCompletedProfile": user_data.get("hasCompletedProfile", False)
            }
            
            print(f"User profile and full name retrieved for user {user_id}")
            return combined_data
        elif profile.exists:
            print(f"Only profile found for user {user_id}, full name missing")
            return profile.to_dict()
        elif user_doc.exists:
            print(f"Only full name found for user {user_id}, profile missing")
            return {"full_name": user_doc.to_dict().get("fullname", "")}
        else:
            print(f"No profile or full name found for user {user_id}")
            return {}
    except Exception as e:
        print(f"Error retrieving user profile for {user_id}: {str(e)}")
        return {}

def update_user_profile(user_id: str, updated_fields: dict):
    try:
        firebase_db = get_firebase_db()
        if firebase_db is None:
            print("⚠️  Firebase not available")
            return
        user_doc_ref = firebase_db.collection("users").document(user_id).collection("userDetails").document("profile")

        
        doc_snapshot = user_doc_ref.get()

        if doc_snapshot.exists:
            user_doc_ref.update(updated_fields)
            print(f"[UPDATE] Mise à jour partielle du profil pour {user_id} avec : {updated_fields}")
        else:
            user_doc_ref.set(updated_fields)
            print(f"[CREATE] Nouveau profil créé pour {user_id} avec : {updated_fields}")
    except Exception as e:
        print(f"[Firestore]  Erreur mise à jour/création du profil utilisateur {user_id} : {str(e)}")

def _save_program_to_firebase(self, program_type: str, program_data: dict, user_id: str):
    try:
        firebase_db = get_firebase_db()

        if firebase_db is None:
            print("⚠️  Firebase not available")
            return
        # Use shared timestamp if provided, otherwise generate new one
        timestamp   = int(datetime.now().timestamp())
        program_id  = f"program_{program_type}_{timestamp}"

        firebase_program = {
            "type": program_type,
            "title": program_data.get("program_title", "Programme Personnalisé"),
            "content": program_data,
            "duration": self.plan_duration_weeks or 4,
            "level": self.user_profile.get("activity_level", "intermediate"),
            "createdAt": datetime.now().isoformat(),
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "active"
        }

        firebase_db.collection(f"users/{user_id}/programs").document(program_id).set(firebase_program)
        print(f"✅ Saved {program_type} program to Firebase: {program_id} for user {user_id}")
        # TODO: Send push notification

    except Exception as e:
        print(f"❌ Error saving program to Firebase: {e}")
        import traceback
        print(traceback.format_exc())

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
        user_profile    = get_user_profile(user_id)
        user_profile    = {
            'mainSport': user_profile.get('mainSport', ''),
            'objective': user_profile.get('objective', ''),
            'sportLevel': user_profile.get('sportLevel', ''),
            'age'       : user_profile.get('age', ''),
            'dietaryHabits' : user_profile.get('dietaryHabits', ''),
            'sportPractice' : user_profile.get('sportPractice', ''),
            'height'    : str(user_profile.get('height', '')) + ' cm',
            'weight'    : str(user_profile.get('weight', '')) + ' kg',
            'gender'    : user_profile.get('gender', ''),
            'activity_level': user_profile.get('activity_level', ''),
        }

        message_type    = ChatMessageType.objects.filter(reference='direct_question').first()
        user_message    = ChatMessage.objects.create(message_type=message_type, chat=chat, user=user_id, message=user_message)

        chat_agent      = Agent.objects.filter(reference='chat_agent').last()
        new_message     = ai_fitness_coach.process_user_message(user_message.message, chat_history, user_profile, user_id)

        message_type    = ChatMessageType.objects.filter(reference='direct_answer').first()
        agent_message   = ChatMessage.objects.create(message_type=message_type, chat=chat, agent=chat_agent, message=new_message)

        update_user_profile(user_id, ai_fitness_coach.user_profile)

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
        for message in chat.get_messaages():
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

        # if user_id is not None:
        #     posts = posts.filter(user=user_id)

        posts_data      = []

        for post in posts:
            posts_data.append({
                'id'            : post.reference,
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
    
    def upload_base64_to_cloudinary(self, base64_data, folder='posts'):
        try:
            # Handle different base64 string formats
            if isinstance(base64_data, str):
                if ';base64,' in base64_data:
                    # Handle data URL format: data:image/png;base64,...
                    header, imgstr = base64_data.split(';base64,', 1)
                    # Extract file extension from the content type
                    if '/' in header:
                        ext = header.split('/')[-1].lower()
                    else:
                        ext = 'jpg'  # Default extension if not specified
                else:
                    # Handle raw base64 string
                    imgstr = base64_data
                    ext = 'jpg'  # Default extension if not specified
                
                # Decode the base64 string
                image_data = base64.b64decode(imgstr)
            else:
                # If it's already bytes, use it directly
                image_data = base64_data
                ext = 'jpg'  # Default extension if not specified
                
            # Generate a unique filename with the appropriate extension
            filename = f"{uuid.uuid4()}.{ext}"
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                image_data,
                folder=folder,
                public_id=filename,
                resource_type='auto'
            )
            
            return {
                'url': result.get('secure_url'),
                'public_id': result.get('public_id'),
                'format': result.get('format')
            }
            
        except Exception as e:
            print(f"Error uploading to Cloudinary: {str(e)}")
            return None
    
    def post(self, request, format=None):
        context = {}

        user_id = request.POST.get('user_id', None)
        content = request.POST.get('content', None)
        base64_attachments = request.POST.getlist('attachements')  # Expecting a list of base64 strings

        if not user_id or not content:
            context['code'] = 400
            context['message'] = "User ID and content are required"
            return JsonResponse(context, status=400)

        if not base64_attachments:
            context['code'] = 400
            context['message'] = "Attachments are required"
            return JsonResponse(context, status=400)

        if not isinstance(base64_attachments, list):
            context['code'] = 400
            context['message'] = "Attachments must be a list"
            return JsonResponse(context, status=400)

        # Process attachments
        attachment_urls = []
        if base64_attachments:
            for base64_data in base64_attachments:
                if not base64_data:
                    continue
                    
                # Upload to Cloudinary
                upload_result = self.upload_base64_to_cloudinary(base64_data)
                if upload_result:
                    attachment_urls.append(upload_result['url'])
        
        # Create the post with attachment URLs as a comma-separated string
        post = Post.objects.create(
            user=user_id,
            content=content,
            attachements=attachment_urls
        )

        context['code'] = 200
        context['data'] = {
            'post': {
                'id': post.reference,
                'attachements': attachment_urls
            }
        }
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
