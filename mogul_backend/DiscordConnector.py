import json
import requests
from discord.ext import commands
from django_discord_connector.request import DiscordRequest
import logging


logger = logging.getLogger(__name__)

class DiscordConnector(DiscordRequest):
    def get_token(self):
        return self.bot_token

    def initiate_dm(self, recipient_id):
        url = "https://discord.com/api/users/@me/channels"
        data = {"recipient_id": recipient_id}
        response = requests.post(url,headers={'Content-Type': 'application/json','Authorization': 'Bot ' + self.bot_token},data=json.dumps(data))
        return response

    @staticmethod
    def get_instance():
        from django_discord_connector.models import DiscordClient
        return DiscordConnector(settings=DiscordClient.get_instance().serialize())