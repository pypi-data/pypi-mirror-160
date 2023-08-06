import asyncio
from asyncio import Future
from functools import singledispatchmethod

from aioprocessing import AioProcess

from web_foundation.kernel import NamedContext
from web_foundation.kernel.isolates.channel import IChannel
from abc import ABCMeta, abstractmethod


class Isolate(metaclass=ABCMeta):
    debug: bool
    _name: str
    _channel: IChannel
    _proc: AioProcess
    _async_mode: bool
    _named_ctx: NamedContext
    _configured: bool

    def __init__(self, async_mode: bool = False, debug: bool = False, configured: bool = False):
        self._async_mode = async_mode
        self.debug = debug
        self._configured = configured

    @property
    def name(self):
        return self._name

    @property
    def ctx(self) -> NamedContext:
        return self._named_ctx

    @ctx.setter
    def ctx(self, value: NamedContext):
        self._named_ctx = value

    @property
    def configured(self) -> bool:
        return self._configured

    @abstractmethod
    async def _run(self):
        pass

    @singledispatchmethod
    def _configure(self, *args, **kwargs):
        pass

    def configure(self, name: str, *args, **kwargs):
        self._name = name
        self._proc = AioProcess(target=self._startup)
        self._channel = IChannel(self._name)
        self._configure(*args, **kwargs)
        self._configured = True

    @abstractmethod
    def _close(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        self._close(*args, **kwargs)

    def _startup(self):
        asyncio.run(self._run())

    async def _exec(self):
        self._proc.start()

    def perform(self) -> Future:
        if not self.configured:
            raise RuntimeError(f"Isolate {self} not configured before start")
        return asyncio.ensure_future(self._exec())

    @property
    def channel(self) -> IChannel:
        return self._channel

    @property
    def pid(self) -> int:
        return self._proc.pid

    @property
    def process(self) -> AioProcess:
        return self._proc
