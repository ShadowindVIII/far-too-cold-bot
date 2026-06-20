from logging import log
import discord
from discord import Bot, Message, ApplicationContext
from discord.ext import commands
from discord.ext.commands import errors
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta, timezone

class Cog(commands.Cog):
  def __init__(self, bot: Bot, client: MongoClient):
    self.bot = bot
    self.client = client

  @commands.command()
  @commands.guild_only()
  @commands.has_guild_permissions(administrator=True)
  @commands.has_role(2222222222222222) # Checks for one role
  @commands.has_any_role('Moderators', 2222222222222222) # Checks for one out of multiple roles
  async def ping(self, ctx: commands.Context):
    await ctx.reply(f'Pong. My latency is {self.bot.latency}')

  @commands.Cog.listener()
  async def on_message(self, message: Message):
    if message.channel.id != 1111111111111111: # replace with your thread's ID
      return
    
    log_channel = self.bot.get_channel(9999999999999999) 
    if not log_channel:
      log_channel = await self.bot.fetch_channel(9999999999999999) 
    await log_channel.send(f'New log: {message.author.mention} said: ```{message.content}```')