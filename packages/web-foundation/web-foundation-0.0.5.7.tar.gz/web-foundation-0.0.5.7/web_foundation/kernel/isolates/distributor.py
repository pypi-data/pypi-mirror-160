import asyncio
from asyncio import Task
from typing import Dict, List

from loguru import logger

from web_foundation.kernel import Isolate
from web_foundation.kernel.isolates.channel import IChannel
from web_foundation.kernel.isolates.pipes import GenericIMessage


class IDistributor:
    channels: Dict[str, IChannel]

    def __init__(self, isolates: List[Isolate]):
        self.channels = {}
        for iso in isolates:
            self.channels.update({iso.name: iso.channel})

    async def on_channel_sent(self, msg: GenericIMessage):
        logger.warning(msg)
        channel: IChannel = self.channels[msg.destination]
        await channel.consume_pipe.write(msg)

    def preform(self) -> List[Task]:
        tasks = []
        for channel in self.channels.values():
            tasks.append(asyncio.ensure_future(
                channel.listen_produce(
                    self.on_channel_sent
                )))
        return tasks
