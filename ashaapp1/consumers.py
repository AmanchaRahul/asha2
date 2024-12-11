import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope["user"]
            self.user_id = self.scope['url_route']['kwargs']['user_id']

            logger.info(f"WebSocket connection attempt for user {self.user_id}")

            # Enhanced authentication check
            if not self.user or not self.user.is_authenticated:
                logger.warning(f"Unauthenticated connection attempt for user {self.user_id}")
                await self.close(code=4003)  # Forbidden
                return

            self.group_name = f"chat_{self.user_id}"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connection established for user {self.user_id}")

        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close(code=1011)  # Internal server error

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected: {close_code}")
        except Exception as e:
            logger.error(f"Disconnect error: {str(e)}")
    
    
    
    @database_sync_to_async
    def get_user_role(self):
        return self.user.userprofile.role
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()

            if not message:
                logger.warning("Received empty message")
                return
            
            user_role = await self.get_user_role()
            
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'user_role': user_role,  # Add user role here
                }
            )
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Message receive error: {str(e)}")

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'user': event['user'],
                'user_role': event['user_role'],  # Include user role in the response
            }))
        except Exception as e:
            logger.error(f"Message send error: {str(e)}")