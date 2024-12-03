import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class Notification(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notify'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # Retrieve necessary data from the event
        notification = event['notification']

        # Send notification to connected clients
        await self.send(text_data=json.dumps(notification))