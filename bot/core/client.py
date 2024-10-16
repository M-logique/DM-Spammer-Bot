from logging import getLogger
from typing import Tuple

from discord import Activity as _Activity
from discord import ActivityType as _ActivityType
from discord import AllowedMentions as _AllowedMentions
from discord import Intents as _Intents
from discord.ext import commands as _commands

from ..templates.embeds import ErrorEmbed
from ..utils.functions import list_all_dirs, search_directory
from ..utils.kvdatabse import KVDatabase
from .logger import Logger as _Logger
from .settings import settings


class Client(_commands.Bot):


    __slots__: Tuple[str, ...] = (
        "logger",
        "db"
    )

    def __init__(
        self, 
        intents: _Intents, 
        allowed_mentions: _AllowedMentions,
        **options
    ):

        self.logger = _Logger("bot", level="INFO")

        owner_ids = settings.OWNERS
        prefix = settings.PREFIX

        self.db = KVDatabase("./data/Database.db")

        super().__init__(
            command_prefix=_commands.when_mentioned_or(*prefix),
            owner_ids=owner_ids,
            strip_after_prefix=True,
            allowed_mentions=allowed_mentions, 
            intents=intents,
            **options
        )

    async def on_ready(self):

        
        await self.change_presence(activity=_Activity(type=_ActivityType.streaming, url="https://twitch.tv/discord", name="github.com/M-logique/DM-Spammer-Bot"))
        if self.cogs != {}: return self.logger.warn("Skipped loading cogs: Reconnecting")

        self.logger.info(f"Discord Client Logged in as {self.user.name}")

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
        log = getLogger("bot.errors")

        formatted_kwargs = " ".join(f"{x}={y}" for x, y in kwargs.items())
        log.error(
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
        log = getLogger("bot.ext")
        for extension in search_directory(path):
            try:

                await self.load_extension(extension)
                log.info("loaded {}".format(extension))
            except Exception as err:

                log.error("There was an error loading {}, Error: {}".format(extension, err))

    def run(self):



        return super().run(
            settings.TOKEN,
            log_handler=self.logger.handler,
            log_formatter=self.logger.formatter,
            log_level=self.logger.level,
            root_logger=self.logger.root
        )