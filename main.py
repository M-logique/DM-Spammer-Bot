import discord

from bot.core.client import Client
from bot.core.settings import settings

client = Client(
                intents=discord.Intents.all(),
                allowed_mentions=discord.AllowedMentions(replied_user=False)
                )



client.run()