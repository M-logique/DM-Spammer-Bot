from discord.ext import commands

from bot.core.client import Client
from bot.templates.cogs import Cog


class TokenTools(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="tokens")
    @commands.is_owner()
    async def _tokens(self, ctx):
        with open("./data/tokens.txt", "r") as file:
            await ctx.reply(str(len(file.readlines())))

    @commands.command(name="append")
    @commands.is_owner()
    async def _append(self, ctx: commands.Context, *,token: str):
        with open("./data/tokens.txt", "a") as fp:
            fp.write("\n"+token)
            await ctx.message.add_reaction("👌🏿")


def setup(client): client.add_cog(TokenTools(client))