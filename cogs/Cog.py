from logging import log
import discord
from discord import Bot, Message, ApplicationContext, Member
from discord.ext import commands
from discord.ext.commands import errors
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta, timezone

class Cog(commands.Cog):
  def __init__(self, bot: Bot):
    self.bot = bot


  @commands.command()
  @commands.guild_only()
  @commands.has_guild_permissions(administrator=True)
  async def ping(self, ctx: commands.Context):
    await ctx.reply(f'Pong. My latency is {self.bot.latency}')

  @commands.Cog.listener()
  async def on_message_delete(self, message: Message):
    log_channel = self.bot.get_channel(1517697376461000807) 
    if not log_channel:
      log_channel = await self.bot.fetch_channel(1517697376461000807) 
    await log_channel.send(f'New log: {message.author.mention} said: ```{message.content}```')

  @commands.Cog.listener()
  async def on_member_update(self, before: Member, after: Member):
    guild = await self.bot.fetch_guild(291184728944410624)
    kick_role = discord.utils.get(guild.roles, name='Kick me out!')
    contacted = ''

    # Skip if user has staff role
    for r in after.roles:
      #role IDs in order: admins, oversight, overseers, trainees, advisory, events, art, story, voice chat, community, first playthrough, gameplay, modding, challenge, helpers
      if r.id in [291207293905928193, 899606559234064425, 291242797975994378, 981423496267702332, 981423394430013470, 1363962684923449364, 896328589572702238, 1191913546284544200, 1422388504297738270, 964852120929046618, 1137895527271379055, 810244997852168192, 870666604940238880, 1092525520010346558, 1147424344209895474]: 
        return

    if kick_role in after.roles:
      try:
        await after.send(content=f"""# Account auto-kicked: Bot detected\nYour account was removed from the server for selecting one of the options on the final onboarding question, called "Are you a human?"\n\nThis question is meant to kick out scam accounts or botted accounts that try to self-assign every role upon joining the server.\n**Please skip the last question and do not select the "I am not a human" option!**\n\nYou may rejoin the server by [clicking here](https://discord.gg/rainworld). If you had level roles, they can be regained by writing `!level up` in https://discord.com/channels/291184728944410624/291185557789343744.""")
      except Exception as e:
        if str(e)[0:3] == '403':
          contacted = '. User had DMs disabled, not contacted.'
          pass
        else:
          raise e

      await self.bot.get_channel(291267111525941248).send(f"# Suspected Bot Autokick\n<@{after.id}> / {after.id}{contacted}")
      await after.remove_roles(kick_role)
      await after.kick(reason=f"Self-selected the bot auto-kick role{contacted}")