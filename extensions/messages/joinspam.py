import discord
from discord.ext import commands

from bot.core.client import Client
from bot.core.settings import settings
from bot.templates.cogs import Cog


class JoinSpam(Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.group(name="spam-on-join", aliases=['onjoin'])
    async def onjoin(self, ctx: commands.Context): ...
    
    @onjoin.command(name="add")
    async def add(self, ctx: commands.Context, user: discord.User):
        if ctx.channel.id != settings.COMMANDS_CHANNEL: return await ctx.reply("The commands are only available at <#%s>" % settings.COMMANDS_CHANNEL)        

        current_status = self.client.db.get(f'{user.id}.spam_on_join')

        if current_status and current_status['status']:
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

        current_status = self.client.db.get(f'{user.id}.spam_on_join')

        if current_status and current_status['status']:
            if current_status['initiator'] != ctx.author.id:
                await ctx.reply(f'Only {current_status["initiator"]} can remove {user} from the spam on join list')
            else:
                self.client.db.delete(f'{user.id}.spam_on_join')
    
async def setup(client): await client.add_cog(JoinSpam(client))