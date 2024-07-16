import asyncio

import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.handlers.joinspam import JoinSpam
from bot.handlers.tools import Tools
from bot.templates.cogs import Cog
from bot.templates.embeds import ErrorEmbed


class OnMemberJoin(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        if JoinSpam.is_in_list(str(member.id)):
            try:
                await member.send("<:tiredskull:1195760828134211594> SEXED BY `Spam On Join`")

                with open("./data/tokens.txt", "r") as file:
                    tokens = [i.strip() for i in file.readlines()]
                
                tasks = [
                    asyncio.ensure_future(Tools.send_message(token, 
                                            member.id, 
                                            "`Auto Join Spam#0`: Hi <:tiredskull:1195760828134211594>"))
                         for token in tokens
                         ]

                await asyncio.gather(*tasks)

                JoinSpam.remove(str(member.id))
                channel = await self.client.fetch_channel(settings.COMMANDS_CHANNEL)
                await channel.send("<:tiredskull:1195760828134211594> Auto Join Spam Applied %s" % member)
            except: 
                pass



async def setup(client): await client.add_cog(OnMemberJoin(client))