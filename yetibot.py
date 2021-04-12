#!/usr/bin/env python

import os
import discord
import random
import logging
import websocket
import websockets
from dotenv import load_dotenv
from django.conf import settings
from discord.ext import commands
import asyncio
from asgiref.sync import sync_to_async,async_to_sync
from a2wsgi import WSGIMiddleware,ASGIMiddleware
from channels.db import database_sync_to_async
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mogul_os.settings")
import django
django.setup()

from notifications.models import Notification
from mogul_backend.models import Transaction
from django_discord_connector.models import DiscordUser,DiscordToken

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    global bot
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

class Greetings(commands.Cog, name="Ciao"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


class Websockets(commands.Cog, name="Websocket Helper"):
    def __init__(self, bot):
        self.bot = bot
        self.wsapp = websocket.WebSocketApp("ws://localhost:8000/ws/discord/broadcast/", on_message=self.on_message)
        self.wsapp.run_forever()

    def on_message(wsapp, message):
        global bot
        channel = bot.get_channel(411224774367248395)
        result = async_to_sync(channel.send)(f"Just received this {message}")



class Yeti(commands.Cog, name="Yeti Commands"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='roll_dice', help='Simulates rolling dice.')
    async def roll(self,ctx , number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(name='create-channel')
    @commands.has_role('admin')
    async def create_channel(self,ctx , channel_name='real-python'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

    @commands.command(name='notify')
    @commands.has_role('admin')
    @sync_to_async
    def get_notifications(self,ctx):
        # Let's find the user
        print(ctx.author.id)
        results = Notification.objects.first()
        print(results)
        result = async_to_sync(ctx.send)(f"Last: {results}")

    @commands.command(name='transaction')
    @sync_to_async
    def get_last_transaction(self,ctx):
        dbuser = DiscordUser.objects.filter(external_id=ctx.author.id).first()
        token = DiscordToken.objects.filter(discord_user_id=dbuser.id).first()
        results = Transaction.objects.filter(user=token.user).order_by('date').last()
        result = async_to_sync(ctx.send)(f"Latest transaction: {results}")


bot.add_cog(Greetings(bot))
bot.add_cog(Yeti(bot))
bot.run(TOKEN)