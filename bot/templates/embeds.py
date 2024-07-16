from datetime import datetime as _datetime
from typing import Any as _Any

from discord import Color as _Color
from discord import Embed as _Embed


class ErrorEmbed(_Embed):


    def __init__(self, error: str,
                *args: _Any, 
                **kwgrs: _Any) -> None:


        super().__init__(title="We Got an Error!",
                        color=_Color.from_rgb(255, 3, 7),
                        description="⚠️ {}".format(error),
                        timestamp=_datetime.now(),
                        *args, 
                        **kwgrs
                    )

