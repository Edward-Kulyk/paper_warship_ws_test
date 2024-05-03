# battleship/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f'game_{self.game_id}'

        # Присоединение к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получение сообщения от клиента
        data = json.loads(text_data)
        # Обработка сообщения
        # Например, отправка обновленных данных всем клиентам в группе комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'data': data
            }
        )

    # Обработчик для отправки сообщения всем клиентам в группе комнаты
    async def game_message(self, event):
        data = event['data']
        # Отправка сообщения клиенту
        await self.send(text_data=json.dumps(data))
