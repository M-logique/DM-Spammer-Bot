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
        if self.client.db.get('spam_on_join_all'):
            cmds_channel = self.client.get_channel(settings.COMMANDS_CHANNEL)
            await cmds_channel.send(f'Spam all on join is enabled')
            try:
                await member.send("🥱 SEXED BY SPAM ALL ON JOIN")

                msg = "{}: {}".format('Zena Bot', 'sexed by spam all on join')[:1500:]

                Tools.send_direct_message(member.id, msg)

                await cmds_channel.send(f'{member} got spammed on joining')
            except:
                await cmds_channel.send(f'Ummm, I got an error while spamming {member} upon joining')

        else:
            spam_on_join = self.client.db.get(f'{member.id}.spam_on_join')
            if spam_on_join and spam_on_join['status']:
                cmds_channel = self.client.get_channel(settings.COMMANDS_CHANNEL)
                await cmds_channel.send(f'{member} has spam on join enabled')
                try:
                    await member.send("🥱 SEXED BY %s" % spam_on_join['initiator'])

                    msg = "{}: {}".format(spam_on_join['initiator'], 'sexed by spam on join')[:1500:]

                    Tools.send_direct_message(member.id, msg)

                    await cmds_channel.send(f'{member} got spammed on joining')
                    self.client.db.delete(f'{member.id}.spam_on_join')
                except:
                    await cmds_channel.send(f'Ummm, I got an error while spamming {member} upon joining')
                    self.client.db.delete(f'{member.id}.spam_on_join')



async def setup(client): await client.add_cog(OnMemberJoin(client))