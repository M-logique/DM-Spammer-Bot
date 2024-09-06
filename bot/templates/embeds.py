from datetime import datetime as _datetime
from typing import Any as _Any

from discord import Color as _Color
from discord import Embed as _Embed


class ErrorEmbed(_Embed):
    """A shitty embed for displaying errors"""

    def __init__(self, error: str,
                *args: _Any, 
                **kwgrs: _Any) -> None:


        super().__init__(
            description=":x: {}".format(error),
            color=_Color.red(),
            *args, 
            **kwgrs
        )

