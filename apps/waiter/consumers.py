# apps/waiter/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.restaurant_id = self.scope['url_route']['kwargs']['restaurant_id']
        self.room_group_name = f'orders_restaurant_{self.restaurant_id}'

        # Join restaurant group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave restaurant group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'new_order':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_new_order',
                    'order_data': text_data_json.get('order_data')
                }
            )

        elif message_type == 'order_status_update':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_order_update',
                    'order_data': text_data_json.get('order_data')
                }
            )

    async def send_new_order(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order_data': event['order_data']
        }))

    async def send_order_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_data': event['order_data']
        }))


class WaiterNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.waiter_id = self.scope['url_route']['kwargs']['waiter_id']
        self.room_group_name = f'notifications_waiter_{self.waiter_id}'

        # Join waiter group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave waiter group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'call_waiter':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_waiter_call',
                    'call_data': text_data_json.get('call_data')
                }
            )

    async def send_waiter_call(self, event):
        await self.send(text_data=json.dumps({
            'type': 'call_waiter',
            'call_data': event['call_data']
        }))
