from django.db.models.signals import post_save
from notifications.signals import notify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
from notifications.models import Notification
from django.contrib.auth.models import User
from mogul_backend.models import Order
import json
import discord
from discord.embeds import Embed
from mogul_backend.DiscordConnector import DiscordConnector
from django.dispatch import Signal

from channels.layers import get_channel_layer
from .serializers import NotificationSerializer

async def update_notifications(notification):
    serializer = NotificationSerializer(notification)
    group_name = serializer.get_group_name()
    channel_layer = get_channel_layer()
    content = {
        # This "type" passes through to the front-end to facilitate
        # our Redux events.
        "type": "UPDATE_NOTIFICATION",
        "payload": serializer.data,
    }
    await channel_layer.group_send(group_name, {
        # This "type" defines which handler on the Consumer gets
        # called.
        "type": "notify",
        "content": content,
    })

@receiver(post_save, sender=Notification)
def send_notification_to_webhook(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    data = model_to_dict(instance)
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    async_to_sync(channel_layer.group_send)("user_notifications",{"type": "stream", "data": json_data})

@receiver(post_save, sender=Notification)
def send_notification_to_discord(sender, instance, **kwargs):
    if isinstance(instance, Order):
        if (instance.is_buy_order is not None) and (instance.is_buy_order is not False):
            buyorder = "buying"
        else:
            buyorder = "selling"
        dembed=Embed(title="Order Completed", description=f"Your order __{buyorder}__ {instance.volume_total} __{instance.item}__ has been {instance.state}", color=0x008080)
        dembed.set_thumbnail(url=f"https://imageserver.eveonline.com/Type/{instance.type_id}_64.png")
        dembed.add_field(name="Status", value=f"{instance.state}", inline=True)
        dembed.add_field(name="Quantities", value=f"{instance.volume_total - instance.volume_remain}/{instance.volume_total}", inline=True)
        dembed.add_field(name="Station", value=f"{instance.station}", inline=True)
        dembed.add_field(name="Range", value=f"{instance.range}", inline=True)
        delta = instance.updated_at - instance.issued
        dembed.add_field(name="Duration", value=f"{delta.days}", inline=True)
        dembed.add_field(name="Character", value=f"{instance.character}", inline=True)
        dembed.add_field(name="Price", value=f"{instance.price}", inline=True)
        dembed.set_footer(text=f"Mogul_OS | {instance.last_updated}")
        instance.recipient.dm_user(embed=dembed)