import discord
from discord.ext import commands

from bot.core.client import Client
from bot.handlers.joinspam import JoinSpam
from bot.templates.cogs import Cog
from bot.utils.functions import chunker


class Premium(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
    
    @commands.command(name="joinspam-add", aliases=["add"])
    async def _add(self, ctx: commands.Context, user: discord.User):
        vip = discord.utils.get(ctx.author.roles, id=1197169168252944435)
        if not vip: return await ctx.reply("This command is available for vip users")

        if not JoinSpam.is_in_list(str(user.id)):
            JoinSpam.append(str(user.id), ctx.author.id)
            await ctx.message.add_reaction("👌🏿")
        else:
            return await ctx.reply("This user is aleardy in list")
        
    @commands.command(name="joinspam-remove", aliases=["remove"])
    async def _remove(self, ctx: commands.Context, user: discord.User):
        vip = discord.utils.get(ctx.author.roles, id=1197169168252944435)
        if not vip: return await ctx.reply("This command is available for vip users")

        if JoinSpam.is_in_list(str(user.id)):
            JoinSpam.remove(str(user.id))
            await ctx.message.add_reaction("👌🏿")
        else:
            return await ctx.reply("This user is not in list")



    @commands.command(name="joinspam-list", aliases=["list"])
    async def _list(self, ctx: commands.Context):
        vip = discord.utils.get(ctx.author.roles, id=1197169168252944435)
        if not vip: return await ctx.reply("This command is available for vip users")


        lst = JoinSpam.user_joinspams(str(ctx.author.id))
        if len(lst) == 0: return await ctx.reply("You don't have any listed user")
        lst = [i.split(":")[0] for i in lst]

        chunks = chunker(lst, 30)

        msg = ctx.message

        for chunk in chunks:
            msg = await msg.reply("```\n%s```" % '\n'.join(chunk))

    @commands.command(name="joinspam-clear", aliases=["clear"])
    async def _clear(self, ctx: commands.Context):
        vip = discord.utils.get(ctx.author.roles, id=1197169168252944435)
        if not vip: return await ctx.reply("This command is available for vip users")


        lst = JoinSpam.user_joinspams(str(ctx.author.id))
        if len(lst) == 0: return await ctx.reply("You don't have any listed user")
        lst = [i.split(":")[0] for i in lst]

        for i in lst:
            JoinSpam.remove(i)
        else:
            await ctx.reply("Removed %s listed user(s)" % len(lst))


async def setup(client): await client.add_cog(Premium(client))