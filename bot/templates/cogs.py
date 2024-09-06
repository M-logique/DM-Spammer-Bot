from discord.ext import commands as _commands

from ..core.client import Client




class Cog(_commands.Cog):

    def __init__(self, client: Client) -> None:
        self.client = client