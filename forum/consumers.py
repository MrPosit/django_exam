import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class ThreadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'thread_{self.thread_id}'

        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )

        logger.info(f'Клиент подключен к теме {self.thread_id}')
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.thread_group_name,
            self.channel_name
        )

        logger.info(f'Клиент отключен от темы {self.thread_id}')

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)['message']
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    'type': 'thread_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Неверный формат сообщения'
            }))

    async def thread_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
