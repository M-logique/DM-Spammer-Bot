import asyncio as _asyncio
from threading import Thread as _Thread
from typing import Any, Coroutine, Sequence


class Thread(_Thread):

    def __init__(self, coroutine: Coroutine, args: Sequence[Any] = None,
                 **options) -> None:

        def wrapper():
            loop = _asyncio.new_event_loop()
            _asyncio.set_event_loop(loop)
            if args:
                loop.run_until_complete(coroutine(*args))
            else:
                loop.run_until_complete(coroutine())

            loop.close()


        super().__init__(target=wrapper,
                         **options)