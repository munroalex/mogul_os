from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User 
from mogul_backend.DiscordConnector import DiscordConnector
# Create your models here.

def dm_user(self,message=None,embed=None):
	disc = DiscordConnector.get_instance()
	channel = self.preferences['notifications__discord_dm_channel']
	try:
		disc.send_channel_message(channel,message=message,embed=embed)
	except:
		pass

User.add_to_class("dm_user",dm_user)