import logging as _logging
from os import makedirs as _makedirs
from os import path as _path

from discord import Activity as _Activity
from discord import ActivityType as _ActivityType
from discord import AllowedMentions as _AllowedMentions
from discord import Intents as _Intents
from discord.ext import commands as _commands

from .. import __name__ as name
from ..templates.embeds import ErrorEmbed
from ..utils.functions import list_all_dirs, search_directory
from .logger import Logger as _Logger
from .settings import settings


class Client(_commands.Bot):


    def __init__(self, intents: _Intents, 
                allowed_mentions: _AllowedMentions,
                **options):

        self.logger = _Logger(name)


        owner_ids = settings.OWNERS
        prefix = settings.PREFIX
        strip_aftre_prefix = settings.STRIP_AFTER_PREFIX

        super().__init__(command_prefix=_commands.when_mentioned_or(*prefix),
                         owner_ids=owner_ids,
                         strip_after_prefix=strip_aftre_prefix,
                         allowed_mentions=allowed_mentions, 
                         intents=intents,
                         **options)

    async def on_ready(self):

        
        await self.change_presence(activity=_Activity(type=_ActivityType.streaming, url="https://twitch.tv/discord", name="TTK - Not tkinter.ttk"))
        if self.cogs != {}: return self.logger.warn("Skipped loading cogs: Reconnecting")

        self.logger.success(f"Discord Client Logged in as {self.user.name}")

        # Cogs loading shits
        self.logger.info("Started loading Extensions")
    
        for dir in list_all_dirs("./extensions"):

            await self.load_extensions(dir)


        self.logger.info("Finished loading Extensions")
        

    
    async def on_command_error(self, ctx: _commands.Context, error: _commands.CommandError):
        if isinstance(error, _commands.CommandNotFound):
            pass
        elif isinstance(error, _commands.MissingPermissions):
            text = "Sorry **{}**, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.reply(embed=ErrorEmbed(text))
        elif isinstance(error, _commands.CommandOnCooldown):
            await ctx.reply(embed=ErrorEmbed(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}s'))
        elif isinstance(error, _commands.NotOwner):
            await ctx.reply(embed=ErrorEmbed("You are not owner"))
        else: 
            if len(str(error)) < 2000:
                await ctx.reply(embed=ErrorEmbed(str(error)))
            else:
                await ctx.reply(embed=ErrorEmbed(str(error)[:2000:]))



    async def on_error(self, event_method: str, /, *args, **kwargs):
        formatted_kwargs = " ".join(f"{x}={y}" for x, y in kwargs.items())
        self.logger.error(
            f"Error in event {event_method}. Args: {args}. Kwargs: {formatted_kwargs}",
            exc_info=True,
        )



    async def load_extensions(self, path: str) -> None:
        """Loads all extensions in a directory.

        .. versionadded:: 2.4

        Parameters
        ----------
        path: :class:`str`
            The path to search for extensions
        """
        for extension in search_directory(path):
            try:

                await self.load_extension(extension)
                self.logger.success("loaded {}".format(extension))
            except Exception as err:

                self.logger.error("There was an error loading {}, Error: {}".format(extension, err))

    def run(self):

        discord_loggers = [
                    'discord',
                    'discord.client',
                    'discord.gateway',
                    'discord.http',
                    'discord.state',
                    'discord.voice',
                    'discord.ext'
                ]
        

        for discord_logger in discord_loggers:
            logger = _logging.getLogger("discord")

            logger.handlers = []

            for handler in self.logger.handlers:

                logger.addHandler(handler)

            logger.setLevel(self.logger.level)

        return super().run(settings.TOKEN)