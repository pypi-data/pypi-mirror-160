from dataclasses import dataclass
from typing import TypeVar

import loguru
from aioprocessing import AioEvent, AioLock, AioQueue  # type: ignore


class IMessage:
    last_idx = 0
    index: int
    sender: str
    destination: str

    def __init__(self, destination: str, idx: int = None):
        self.destination = destination
        if not idx:
            IMessage.last_idx += 1
            self.index = IMessage.last_idx
        else:
            self.index = idx

    def __str__(self):
        return f"IMessage(id={self.index}, dest={self.destination}, sender={self.sender})"


GenericIMessage = TypeVar("GenericIMessage", bound=IMessage, contravariant=True)


@dataclass
class IsolatePipes:
    queue: AioQueue
    event: AioEvent
    lock: AioLock

    async def write(self, msg: GenericIMessage):
        await self.queue.coro_put(msg)

    async def read(self) -> GenericIMessage:
        return await self.queue.coro_get()

    def empty(self):
        return self.queue.empty()
