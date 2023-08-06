import asyncio
from asyncio import Task

from web_foundation.workers.background.message import TaskIMessage, TaskReplyIMessage
from web_foundation.workers.worker import Worker


class TaskExecutor(Worker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _configure(self, *args, **kwargs):
        pass

    async def _run(self):
        await self.channel.listen_consume(self.task_handler)

    async def task_handler(self, message: TaskIMessage):
        task = asyncio.create_task(self.exec(message))
        if message.respond:
            task.add_done_callback(self.produce_response)

    async def exec(self, msg: TaskIMessage) -> TaskReplyIMessage:
        return TaskReplyIMessage(msg, await msg.task(msg), self.name)

    def produce_response(self, resp: Task):
        asyncio.create_task(self.channel.produce(resp.result()))

    def _close(self,*args,**kwargs):
        pass
