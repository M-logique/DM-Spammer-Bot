from bot.core.client import Client
import discord
from bot.core.settings import settings

client = Client(
                intents=discord.Intents.all(),
                allowed_mentions=discord.AllowedMentions(replied_user=False)
                )



client.run(settings.TOKEN)