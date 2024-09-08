import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog
from bot.utils.tools import Tools


class OnMemberJoin(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        commands_channel = member.guild.get_channel(settings.COMMANDS_CHANNEL)

        if not commands_channel:
            return # to prevent other servers using spam on join

        spam_on_join = self.client.db.get(f'{member.id}.spam_on_join') or {}
        protection = self.client.db.get(f"{member.id}.protected")
        if protection: return 
        if self.client.db.get('spam_on_join_all'):
            # await cmds_channel.send(f'Spam all on join is enabled')
            try:
                await member.send("🥱 SEXED BY SPAM ALL ON JOIN")
                msg = "{}: {}".format('Zena Bot', 'sexed by spam all on join')[:1500:]
                Tools.send_direct_message(member.id, msg)
                await commands_channel.send(f'{member} got spammed on joining')
                if spam_on_join.get("status"):
                    self.client.db.delete(f'{member.id}.spam_on_join')
            except:
                await commands_channel.send(f'Ummm, I got an error while spamming {member} upon joining')

        elif spam_on_join.get('status'):
            await commands_channel.send(f'{member} has spam on join enabled')
            try:
                await member.send("🥱 SEXED BY %s" % spam_on_join['initiator'])
                msg = "{}: {}".format(spam_on_join['initiator'], 'sexed by spam on join')[:1500:]
                Tools.send_direct_message(member.id, msg)
                await commands_channel.send(f'{member} got spammed on joining')
                self.client.db.delete(f'{member.id}.spam_on_join')
            except:
                await commands_channel.send(f'Ummm, I got an error while spamming {member} upon joining')



async def setup(client): await client.add_cog(OnMemberJoin(client))