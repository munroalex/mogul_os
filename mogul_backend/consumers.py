from . import models
from . import serializers
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import InvalidChannelLayerError, StopConsumer
from channels.consumer import AsyncConsumer
from notifications.models import Notification
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)


class NotificationConsumer(AsyncConsumer):
    groups = ["user_notifications"]

    async def websocket_connect(self, event):
        print("connected", event)
        await self.channel_layer.group_add("user_notifications",self.channel_name)
        await self.send({
            "type": "websocket.accept"
        })

    async def stream(self, event):

        await self.send({
           'type': 'websocket.send',
           'text': event.get('data')
        })

class DiscordConsumer(AsyncConsumer):
    groups = ["discord"]

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        pass

    async def websocket_connect(self, event):
        print("connected", event)
        await self.channel_layer.group_add("discord_broadcast",self.channel_name)
        await self.send({
            "type": "websocket.accept"
        })

    async def stream(self, event):

        await self.send({
           'type': 'websocket.send',
           'text': event.get('data')
        })