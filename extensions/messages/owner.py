import ast
import datetime

import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog

MAIN_COLOR = discord.Color.from_rgb(*settings.MAIN_COLOR)

class Buttons(discord.ui.View):
    def __init__(self, author, chunk) -> None:

        super().__init__(timeout=180)
        super().add_item(self.Buttons(author=author, label="<<<", chunk=chunk))
        super().add_item(self.Buttons(author=author, label=">>>", chunk=chunk))


    class Buttons(discord.ui.Button):  # Button class
        def __init__(self, label, author, chunk):
            self.chunk, self.author = chunk, author
            self.index = 0
            super().__init__(label=label, style=discord.ButtonStyle.secondary)  # set label and super init class

        async def callback(self, interaction: discord.MessageInteraction):
            if interaction.author.id != self.author: return await interaction.response.send_message(content="This is not yours", ephemeral=True)
            if interaction.component.label == ">>>":
                if self.index == len(self.chunk)-1:
                    self.index = 0
                else:
                    self.index+=1
                    
                embed = discord.Embed(description=self.chunk[self.index],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (self.index+1, len(self.chunk)), icon_url=interaction.author.avatar)
                await interaction.response.edit_message(embed=embed)
            elif interaction.component.label == "<<<":
                if self.index == 0:
                    self.index = len(self.chunk)-1
                else:
                    self.index-=1
                embed = discord.Embed(description=self.chunk[self.index],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (self.index+1, len(self.chunk)), icon_url=interaction.author.avatar)
                await interaction.response.edit_message(embed=embed)

def chunker(text, chunk_size: int) -> list:
    length = len(text)
    num = 0
    chunks = []

    while num < len(text):
        chunks.append(text[num:length-(length-(chunk_size))+num:])
        num+=chunk_size

    return chunks

def insert_returns(body):
    # insert return stmt if the last expression is an expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Owner(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="delinvites")
    @commands.is_owner()
    async def zena_ba_invita(self, ctx: commands.Context):
        invites = await ctx.guild.invites()
        await ctx.send("<:tiredskull:1195760828134211594> Zenaing with %s invites" % len(invites))
        for invite in invites:
            await invite.delete()
            await ctx.send("%s deleted <:tiredskull:1195760828134211594> " % invite.code)
        else:
            await ctx.send("%s <:tiredskull:1195760828134211594> Zena success" % ctx.author.mention)


    @commands.command(name="eval", aliases=["e"],
                      usage="<code>")
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, code: str):
        fn_name = "_eval_expr"
        cmd = code.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)
        env = {
            'client': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = str((await eval(f"{fn_name}()", env)))
        if result != "None":
            if len(result) < 4000:
                await ctx.send(embed=discord.Embed(color=MAIN_COLOR, description=result, title="Evaluation result", timestamp=datetime.datetime.now()))
            else:
                chunks = chunker(result, chunk_size=4000)
                embed = discord.Embed(description=chunks[0],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (1, len(chunks)), icon_url=ctx.author.avatar)

                await ctx.send(view=Buttons(author=ctx.author.id, chunk=chunks), embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description="*There is no Evaluation result*", timestamp=datetime.datetime.now(), color=MAIN_COLOR))


async def setup(client): await client.add_cog(Owner(client))