import asyncio
from typing import Coroutine, Callable

from aioprocessing import AioQueue, AioEvent, AioLock
from loguru import logger

from web_foundation.kernel.isolates.pipes import IsolatePipes, IMessage


class IChannel:
    read_timeout = 0.01
    pipes: IsolatePipes
    name: str
    debug: bool

    def __init__(self, wroker_name: str, debug: bool = False):
        self.name = wroker_name
        self.debug = debug
        self.produce_pipe = IsolatePipes(AioQueue(), AioEvent(), AioLock())
        self.consume_pipe = IsolatePipes(AioQueue(), AioEvent(), AioLock())

    def __str__(self):
        return f"IChannel(name={self.name})"

    async def produce(self, msg: IMessage):
        msg.sender = self.name
        logger.warning(msg)
        await self.produce_pipe.write(msg)

    async def _listen(self, pipe: IsolatePipes, callback: Callable[[IMessage], Coroutine]):
        while True:
            if pipe.empty():
                await asyncio.sleep(self.read_timeout)
            r: IMessage = await pipe.read()
            if self.debug:
                logger.info(f"Channel {self.name} {'send' if pipe == self.produce_pipe else 'receive'} message: {r}")
            await callback(r)

    async def listen_produce(self, callback: Callable[[IMessage], Coroutine]):
        await self._listen(self.produce_pipe, callback)

    async def listen_consume(self, callback: Callable[[IMessage], Coroutine]):
        await self._listen(self.consume_pipe, callback)
