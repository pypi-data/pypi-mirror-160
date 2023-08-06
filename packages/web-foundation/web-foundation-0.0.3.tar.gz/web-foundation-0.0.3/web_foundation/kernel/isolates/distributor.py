import asyncio
from asyncio import Future
from typing import Dict, List
from web_foundation.kernel import Isolate
from web_foundation.kernel.isolates.channel import IChannel
from web_foundation.kernel.isolates.pipes import IMessage
from loguru import logger


class IDistributor:
    channels: Dict[str, IChannel]

    def __init__(self, isolates: List[Isolate]):
        self.channels = {}
        for iso in isolates:
            self.channels.update({iso.name: iso.channel})

    async def on_channel_sent(self, msg: IMessage):
        logger.warning(msg)
        await self.channels.get(msg.destination).consume_pipe.write(msg)

    def preform(self) -> List[Future]:
        tasks = []
        for channel in self.channels.values():
            tasks.append(asyncio.ensure_future(
                channel.listen_produce(
                    self.on_channel_sent
                )))
        return tasks