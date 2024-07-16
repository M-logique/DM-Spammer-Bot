import asyncio as _asyncio
from threading import Thread as _Thread
from typing import Any, Coroutine, Sequence


class Thread(_Thread):

    def __init__(self, coroutines: Sequence[Coroutine], args: Sequence[Any] = None,
                 **options) -> None:

        def wrapper():
            loop = _asyncio.new_event_loop()
            _asyncio.set_event_loop(loop)
            tasks = [_asyncio.ensure_future(corountine, loop=loop) for corountine in coroutines]

            loop.run_until_complete(_asyncio.gather(*tasks))

            loop.close()


        super().__init__(target=wrapper,
                         **options)