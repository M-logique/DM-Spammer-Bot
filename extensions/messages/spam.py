import asyncio

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


        protected = self.client.db.get(f"{ctx.author.id}.protected")

        if protected: 
            return await ctx.reply("This user is protected <:tiredskull:1195760828134211594>")

        try:
            await user.send("🥱 SEXED BY %s" % ctx.author)
            


            msg = "{}: {}".format(ctx.author, msg)[:1500:]

            Tools.send_direct_message(user.id, msg)

            await ctx.message.add_reaction("<:tiredskull:1195760828134211594>")
        except:
            await ctx.reply("<:tiredskull:1195760828134211594> Error sex")

    # @commands.command(name="message" , aliases=["msg"])
    # @commands.cooldown(1, 120, commands.BucketType.member)
    # async def messager(self, ctx: commands.Context, user: discord.Member, *, message: str = "ZENA"):
    #     if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % COMMANDS_CHANNEL)
    #     captcha = discord.utils.get(ctx.author.roles, id=1198253035370074272)
    #     if not captcha:
    #         return await ctx.reply("> You need <@&1198253035370074272> For using commands, click the link below to claim it\n> شما برای استفاده کردن از کامند ها به رول <@&1198253035370074272> نیاز دارید. روی لینک زیر بزنید تا انرا دریافت کنید\n\n > https://restorecord.com/verify/1195433138013339729", allowed_mentions=discord.AllowedMentions(roles=False), suppress_embeds=True)
    #     if protected(user.id): return await ctx.reply("This user is protected <:tiredskull:1195760828134211594>")

    #     sex_channel = None
    #     channels = [i for i in ctx.guild.channels]
    #     kir_channels = []
    #     for channel in channels:
    #         if channel.category and channel.category.id == 1195794089954770944:
    #             kir_channels.append(channel.id)
    #     else:        
    #         sex_channel = random.choice(kir_channels)
    #         with open("./data/tokens.txt", "r") as file:
    #             tokens = [i.strip() for i in file.readlines()]
    #         await ctx.reply("Sending in <#%s>" % sex_channel)
    #         if sex_channel:
    #             sexnd = lambda msg: req.post(Tools.api("channels/%s/messages" % sex_channel), json={
    #                 "embeds": [
    #                     {
    #                         "description": str(ctx.author)+": "+msg[:1000:]
    #                     }
    #                 ],
    #                 "content": str(user.mention)
    #             },
    #             headers={"Authorization": "Bot "+token})
    #             for token in tokens:
    #                 Thread(target=sexnd, args=(message, )).start()

    #         else:
    #             await ctx.message.add_reaction("✅")

async def setup(client): await client.add_cog(Spam(client))