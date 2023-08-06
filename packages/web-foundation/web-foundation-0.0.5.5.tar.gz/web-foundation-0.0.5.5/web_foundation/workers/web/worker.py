import asyncio
import os
import socket
from typing import List, Type, Any
from functools import singledispatchmethod
from pydantic import BaseModel as PDModel
from sanic import Sanic
from sanic.server.socket import bind_socket

from web_foundation.kernel import NamedContext
from web_foundation.workers.web.sanic_ext.pipline_ext import Pipeline, PipelinesExt
from web_foundation.workers.worker import Worker


class StreamingConf(PDModel):
    listen_timeout: float
    ping_timeout: float


class ServerConfig(PDModel):
    host: str
    port: int
    streaming: StreamingConf | None


class WebServer(Worker):
    config: ServerConfig
    pipelines_ext: PipelinesExt

    def __init__(self, config: ServerConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    @singledispatchmethod
    def _configure(self, *args, **kwargs):
        pass

    @_configure.register
    def _(self, ctx: NamedContext, sock: socket.socket = None):
        self.socket = sock if sock else self.create_socket(self.config)
        self.sanic_app = Sanic(self.name)
        self.sanic_app.after_server_stop(self.close)
        self.sanic_app.ctx.named_ctx = ctx
        self.sanic_app.ctx.channel = self.channel
        self.pipelines_ext = PipelinesExt()

    def add_pipelines(self, pipelines: List[Type[Pipeline]] | Type[Pipeline]):
        if isinstance(pipelines, list):
            self.pipelines_ext.pipelines = pipelines
        else:
            self.pipelines_ext.pipelines.append(pipelines)

    def _init_ext(self):
        self.sanic_app.extend(extensions=[self.pipelines_ext], config={})

    async def _run(self):
        await self.initiate_on_up(self.initiators)
        self._init_ext()

    def _startup(self):
        super(WebServer, self)._startup()
        try:
            self.sanic_app.run(sock=self.socket)
        except KeyboardInterrupt:
            self._close()

    def _close(self, *args, **kwargs):
        self.socket.close()

    @staticmethod
    def create_socket(config: ServerConfig) -> socket.socket:
        sock = bind_socket(config.host, config.port)
        sock.set_inheritable(True)
        return sock
