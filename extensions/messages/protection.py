import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog
from bot.utils.tools import Tools


class Protection(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client


    @commands.command(name="protect")
    async def _protect(self, ctx: commands.Context):
        """Toggles your protection state"""
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        protecttion_state = self.client.db.get(f"{ctx.author.id}.protected")
        new_protecttion_state = not bool(protecttion_state)
        
        state = "Enabled" if new_protecttion_state else "Disabled"

        self.client.db.set(f"{ctx.author.id}.protected", new_protecttion_state)

        await ctx.reply(f"{state} your protection.")



    @commands.command(name="admin-protect")
    @commands.is_owner()
    async def _adminprotect(self, ctx: commands.Context, user: discord.User):
        """Toggles protection for another user (Admin only)"""
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        protecttion_state = self.client.db.get(f"{user.id}.protected")
        new_protecttion_state = not bool(protecttion_state)
        
        state = "Enabled" if new_protecttion_state else "Disabled"
        self.client.db.set(f"{user.id}.protected", new_protecttion_state)

        await ctx.reply(f"{state} {user.name}'s protection.")

    

    @commands.command(name="unprotected")
    @commands.is_owner()
    async def _unprotected(self, ctx: commands.Context):
        """Displays a list of unprotected users in the ctx.guild (Admin only)"""
        
        protected = lambda user_id, /: bool(self.client.db.get(f"{user_id}.protected"))

        unprotected = [
            f"{i.name} - {i.id}"
            for i in ctx.guild.members
            if not protected(i.id)
        ]


        chunks = Tools.chunker(unprotected, 30)

        msg = ctx.message

        for chunk in chunks:
            msg = await msg.reply("```\n%s```" % '\n'.join(chunk))

    @commands.command(name="protected")
    @commands.is_owner()
    async def _protected(self, ctx: commands.Context):
        """Displays a list of protected users in the ctx.guild (Admin only)"""
        
        protected = lambda user_id, /: bool(self.client.db.get(f"{user_id}.protected"))

        unprotected = [
            f"{i.name} - {i.id}"
            for i in ctx.guild.members
            if protected(i.id)
        ]


        chunks = Tools.chunker(unprotected, 30)

        msg = ctx.message

        for chunk in chunks:
            msg = await msg.reply("```\n%s```" % '\n'.join(chunk))


async def setup(client): await client.add_cog(Protection(client))