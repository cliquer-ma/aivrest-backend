import json
import logging
from typing import Dict, Any, Optional

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)

class LiveChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id: Optional[str] = None
        self.room_group_name: Optional[str] = None
        self.user = None

    def _get_required_field(self, data: Dict[str, Any], field: str, message_type: str = 'error') -> Any:
        """Helper to get required field from data with proper error handling"""
        if field not in data:
            error_msg = f"Missing required field: {field}"
            logger.warning(error_msg, extra={'data': data})
            self.send(text_data=json.dumps({
                'type': message_type,
                'message': error_msg
            }))
            raise ValueError(error_msg)
        return data[field]

    def _validate_message_data(self, data: Dict[str, Any]) -> bool:
        """Validate incoming message data"""
        required_fields = ['content', 'message_type', 'from_user']
        try:
            for field in required_fields:
                self._get_required_field(data, field)
            return True
        except ValueError:
            return False

    def connect(self):
        try:
            # Get room reference from URL
            self.room_id = self.scope["url_route"]["kwargs"].get("reference")
            if not self.room_id:
                self.close(code=4000)  # Custom close code for invalid room
                return

            # Get user from scope if authenticated
            self.user = self.scope.get('user')
            
            # Verify room exists and user has access
            LiveChatRoom = apps.get_model("livechat", "LiveChatRoom")
            try:
                room = LiveChatRoom.objects.get(reference=self.room_id)
                if self.user and self.user.id not in room.users:
                    logger.warning(f"User {self.user.id} not authorized for room {self.room_id}")
                    self.close(code=4001)  # Custom close code for unauthorized
                    return
            except ObjectDoesNotExist:
                logger.warning(f"Room not found: {self.room_id}")
                self.close(code=4004)  # Custom close code for not found
                return

            self.room_group_name = f"livechat_{self.room_id}"

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            logger.info(f"User {getattr(self.user, 'id', 'anonymous')} connected to room {self.room_id}")
            self.accept()

        except Exception as e:
            logger.exception("Error in WebSocket connect")
            self.close(code=4003)  # Custom close code for server error

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name') and self.room_group_name:
            try:
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name, self.channel_name
                )
                logger.info(f"User {getattr(self.user, 'id', 'anonymous')} disconnected from room {self.room_id}")
            except Exception as e:
                logger.exception(f"Error during WebSocket disconnect: {str(e)}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            if not text_data:
                raise ValueError("No text data received")

            try:
                data = json.loads(text_data)
            except json.JSONDecodeError:
                error_msg = "Invalid JSON format"
                logger.warning(error_msg, extra={'text_data': text_data})
                self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': error_msg
                }))
                return

            if not self._validate_message_data(data):
                return

            try:
                LiveChatRoom = apps.get_model("livechat", "LiveChatRoom")
                LiveChatMessage = apps.get_model("livechat", "LiveChatMessage")
                LiveChatMessageType = apps.get_model("livechat", "LiveChatMessageType")

                # Get message type
                message_type_ref = data["message_type"]
                message_type = LiveChatMessageType.objects.filter(reference=message_type_ref).first()
                if not message_type:
                    raise ObjectDoesNotExist(f"Message type '{message_type_ref}' not found")

                # Get room
                room = LiveChatRoom.objects.filter(reference=self.room_id).first()
                if not room:
                    raise ObjectDoesNotExist(f"Room '{self.room_id}' not found")

                # Validate user is a participant
                from_user = data["from_user"]
                if from_user not in room.users:
                    raise ValidationError("User is not a participant in this room")

                # Determine recipient
                room_users = room.users
                to_user = next((u for u in room_users if u != from_user), None)
                if not to_user:
                    raise ValidationError("No recipient found in the room")

                # Create message
                live_chat_message = LiveChatMessage.objects.create(
                    room=room,
                    message_type=message_type,
                    content=data["content"],
                    from_user=from_user,
                    to_user=to_user,
                )
                logger.info(f"Message created: {live_chat_message.id} in room {self.room_id}")

                context = {
                    'type': 'chat.message',
                    'chat_message': {
                        'reference': live_chat_message.reference,
                        'content': live_chat_message.content,
                        'message_type': message_type.reference,
                        'content': live_chat_message.content,
                        'message_type': message_type.reference,
                        'from_user': from_user,
                        'to_user': to_user,
                        'created_at': live_chat_message.created_at.isoformat(),
                        'message_id': str(live_chat_message.id),
                        'status': 'delivered'
                    }
                }

                try:
                    # Send message to room group
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, context
                    )
                except Exception as e:
                    logger.exception("Error sending message to room group")
                    # Update message status to failed
                    live_chat_message.status = 'failed'
                    live_chat_message.save(update_fields=['status'])
                    # Notify sender about the failure
                    self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Failed to send message',
                        'message_id': str(live_chat_message.id),
                        'status': 'failed'
                    }))

            except Exception as e:
                logger.exception("Error processing message")
                self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Failed to process message'
                }))

        except Exception as e:
            logger.exception("Error in WebSocket receive")
            self.close(code=4003)  # Custom close code for server error

    # Receive message from room group
    def chat_message(self, event):
        try:
            # Send message to WebSocket
            self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.exception("Error sending message to WebSocket")
            # If we can't send to the WebSocket, close the connection
            self.close(code=4002)  # Custom close code for send error
