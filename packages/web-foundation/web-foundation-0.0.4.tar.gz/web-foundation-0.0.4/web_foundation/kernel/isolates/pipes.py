from dataclasses import dataclass

import loguru
from aioprocessing import AioEvent, AioLock, AioQueue


class IMessage:
    last_idx = 0
    index: int
    sender: int
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


@dataclass
class IsolatePipes:
    queue: AioQueue
    event: AioEvent
    lock: AioLock

    async def write(self, msg: IMessage):
        await self.queue.coro_put(msg)

    async def read(self) -> IMessage:
        return await self.queue.coro_get()

    def empty(self):
        return self.queue.empty()
