from functools import partial
from typing import Callable, Coroutine, Tuple, Dict, Any

from web_foundation.kernel import IMessage

BgTask = Callable[[IMessage, ...], Coroutine[Any, Any, IMessage | None]] | partial


class TaskIMessage(IMessage):
    task: BgTask
    args: Tuple
    kwargs: Dict
    respond: bool

    def __init__(self, destination: str, task: BgTask, args: Tuple = None, kwargs: Dict = None, respond: bool = False):
        super().__init__(destination)
        self.task = task
        self.respond = respond
        self.args = args if args else tuple()
        self.kwargs = kwargs if kwargs else {}


class TaskReplyIMessage(IMessage):
    response: Any

    def __init__(self, task_msg: TaskIMessage, response: Any, sender: str):
        super().__init__(task_msg.sender, task_msg.index)
        self.response = response
        self.sender = sender
