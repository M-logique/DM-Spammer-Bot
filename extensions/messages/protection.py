import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog
from bot.utils.functions import chunker, protected


class Protection(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client


    @commands.command(name="protect")
    async def _protect(self, ctx: commands.Context):
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        with open("./data/protected.txt", "r") as file:
            protected_list = [i.strip() for i in file.readlines()]
        protected = False

        if str(ctx.author.id) in protected_list:
            protected_list.remove(str(ctx.author.id))
            protected = False
        else:
            protected_list.append(str(ctx.author.id))
            protected = True
        
        with open("protected.txt", "w") as file:
            file.write('\n'.join(protected_list))

        if protected:
            await ctx.reply("<:tiredskull:1195760828134211594> Protected %s" % ctx.author)
        else:
            await ctx.reply("<:tiredskull:1195760828134211594> unprotected %s" % ctx.author)



    @commands.command(name="admin-protect")
    @commands.is_owner()
    async def _adminprotect(self, ctx: commands.Context, user: discord.User):
        with open("./data/protected.txt", "r") as file:
            protected_list = [i.strip() for i in file.readlines()]
        
        

        protected = False

        if str(user.id) in protected_list:
            protected_list.remove(str(user.id))
            protected = False
        else:
            protected_list.append(str(user.id))
            protected = True
        
        with open("protected.txt", "w") as file:
            file.write('\n'.join(protected_list))

        if protected:
            await ctx.reply("<:tiredskull:1195760828134211594> Protected %s" % user)
        else:
            await ctx.reply("<:tiredskull:1195760828134211594> unprotected %s" % user)
    

    @commands.command(name="unprotected")
    @commands.is_owner()
    async def _unprotected(self, ctx: commands.Context):
        key = lambda member: not protected(member.id) and not member.bot
        unprotected = [i for i in filter(key, ctx.guild.members)]

        lst = ["%s - %s" % (i, i.id) for i in unprotected]

        chunks = chunker(lst, 30)

        msg = ctx.message

        for chunk in chunks:
            msg = await msg.reply("```\n%s```" % '\n'.join(chunk))

    @commands.command(name="protected")
    @commands.is_owner()
    async def _protected(self, ctx: commands.Context):
        key = lambda member: protected(member.id) and not member.bot
        unprotected = [i for i in filter(key, ctx.guild.members)]

        lst = ["%s - %s" % (i, i.id) for i in unprotected]

        chunks = chunker(lst, 30)

        msg = ctx.message

        for chunk in chunks:
            msg = await msg.reply("```\n%s```" % '\n'.join(chunk))


async def setup(client): await client.add_cog(Protection(client))