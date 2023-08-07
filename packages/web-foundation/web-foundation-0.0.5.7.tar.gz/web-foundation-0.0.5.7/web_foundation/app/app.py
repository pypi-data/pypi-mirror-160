import asyncio
import json
from asyncio import Future
from pathlib import Path
from typing import List, Type, TypeVar, Generic

from pydantic import BaseModel as PdModel
from pyee import AsyncIOEventEmitter

from web_foundation.app.service.service import Service
from web_foundation.kernel import NamedContext
from web_foundation.kernel.isolates.isolate import Isolate

AppConfig = TypeVar("AppConfig", bound=PdModel)


class App(Generic[AppConfig]):
    emitter: AsyncIOEventEmitter
    config: AppConfig
    name: str
    isolates: List[Isolate]
    services: List[Service]
    ctx: NamedContext
    debug: bool

    def __init__(self, name: str, debug: bool = False):
        self.debug = debug
        self.emitter = AsyncIOEventEmitter()
        self.name = name
        self.ctx = NamedContext()
        self.services = []
        self.isolates = []

    def load_config(self, conf_path: Path, config_model: Type[AppConfig]) -> None:
        """
        Load app config to user in
        :param conf_path:
        :param config_model: BaseModel to cast json file to pydantic
        :return: None
        """
        with open(conf_path, "r") as _json_file:
            conf = config_model(**json.loads(_json_file.read()))
            self.config = conf
            self.ctx.app_config = conf

    def add_isolate(self, isolate: Isolate):
        """
        Set isolate to app and set isolate debug and name
        :param isolate: isolate to apply
        :return: None
        """
        if not isolate.configured:
            raise RuntimeError("Isolate not configured")
        isolate.debug = self.debug
        isolate.ctx = self.ctx
        self.isolates.append(isolate)

    def add_service(self, service: Service):
        """
        Set service to use in app
        Set service to named contex
        :param service: service to set
        :return: None
        """
        self.ctx.set_obj(service, kind=Service)
        self.services.append(service)

    async def prepare_infrastructure(self):
        """
        example:
            initor = Provider.of(DatabaseInitiator, self.name)
            for service in self.services:
                await service.prepare(**kwargs : Dict[str, Initiator])
            self.emitter.emit("finalize_init")
        """
        pass

    def perform(self) -> List[Future]:
        """
        Call performs from isolates and return all isolates Futures
        :return: None
        """
        return [isolate.perform() for isolate in self.isolates]

    async def run(self):
        """
        Func to run app manually (without Runner)
        :return: None
        """
        return await asyncio.wait([isolate.perform() for isolate in self.isolates])
