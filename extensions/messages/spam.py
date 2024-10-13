import random

import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog
from bot.templates.embeds import ErrorEmbed
from bot.utils.tools import Tools


class Spam(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
    
    @commands.command(name="spam")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _spam(self, ctx: commands.Context, user: discord.Member, *, msg: str = "Sex 😳"):
        if ctx.channel.id != settings.COMMANDS_CHANNEL:
            return await ctx.reply(
                embed=ErrorEmbed("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)
            )


        protected = bool(self.client.db.get(f"{user.id}.protected"))

        if protected: 
            return await ctx.reply("This user is protected <:tiredskull:1195760828134211594>")

        try:
            await user.send("🥱 SEXED BY %s" % ctx.author)


            msg = "{}: {}".format(ctx.author, msg)[:1500:]

            Tools.send_direct_message(user.id, msg)

            await ctx.message.add_reaction("<:tiredskull:1195760828134211594>")
        except:
            await ctx.reply("<:tiredskull:1195760828134211594> Error sex")

    @commands.group(name="spam-on-join", aliases=['onjoin'])
    async def onjoin(self, ctx: commands.Context): ...
    
    @onjoin.command(name="add")
    async def add(self, ctx: commands.Context, user: discord.User):
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        current_status = self.client.db.get(f'{user.id}.spam_on_join') or {}

        if current_status.get("status"):
            await ctx.reply(f'{user} is already in the spam_on_join list')
        else:
            json = {
                'status': True,
                'initiator': ctx.author.id
            }
            self.client.db.set(f'{user.id}.spam_on_join', json)
            await ctx.reply(f'Added {user} to spam on join')

    @onjoin.command(name="remove", aliases=['del', 'delete'])
    async def remove(self, ctx: commands.Context, user: discord.User):
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        current_status = self.client.db.get(f'{user.id}.spam_on_join') or {}

        if current_status.get("status"):
            if current_status.get("initiator") != ctx.author.id:
                await ctx.reply(f'Only {current_status["initiator"]} can remove {user} from the on join list')
            else:
                self.client.db.delete(f'{user.id}.spam_on_join')

    @onjoin.command(name='all')
    @commands.is_owner()
    async def all(self, ctx: commands.Context):
        current_status = self.client.db.get(f'spam_on_join_all')
        status = not bool(current_status)

        self.client.db.set(f'spam_on_join_all', status)

        await ctx.reply(f'on join for all is now set to: {status}')

    @commands.command(name="message" , aliases=["msg"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def messager(self, ctx: commands.Context, user: discord.Member, *, message: str = "ZENA"):
        if ctx.channel.id != settings.COMMANDS_CHANNEL:
            return await ctx.reply(
                embed=ErrorEmbed("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)
            )
        
        protected = bool(self.client.db.get(f"{user.id}.protected"))

        if protected: 
            return await ctx.reply("This user is protected <:tiredskull:1195760828134211594>")

        channels = [str(channel.id)
            for channel in ctx.guild.channels 
            if channel.category 
            and channel.category.id == 1195794089954770944
        ]
        
        msg = "{}: {}".format(ctx.author, message)[:1500:]
        Tools.send_channel_message(','.join(channels), msg, user.id)
        await ctx.message.add_reaction("<:tiredskull:1195760828134211594>")

async def setup(client): await client.add_cog(Spam(client))