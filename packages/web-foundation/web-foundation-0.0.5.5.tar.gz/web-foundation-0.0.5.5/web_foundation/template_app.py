import asyncio
import os
import pathlib
import warnings
from signal import signal as signal_func, SIGINT, SIGTERM, Signals
from typing import List

from loguru import logger
from pydantic import BaseModel as PDModel

from web_foundation.app import App
from web_foundation.app import AbstractDbModel
from web_foundation.app import AccessService, AccessSpec
from web_foundation.app import Service
from web_foundation.app.infrastructure.database.initiator import DbConfig
from web_foundation.kernel import IDistributor
from web_foundation.workers import TaskIMessage, TaskExecutor, PipelinedRouteConf
from web_foundation.workers import ServerConfig, WebServer
from web_foundation.workers import set_to_pipline, Pipeline, mark_pipelined, Protector
from web_foundation.workers import HTTPMethod, ProtectIdentity, InputContext

warnings.filterwarnings("ignore")  # TODO apply to settings


class AppConfg(PDModel):
    server: ServerConfig
    db_config: DbConfig


class AppBaseService(Service):
    pass


class AnyAppPipeline(Pipeline):
    routes_confs: List[PipelinedRouteConf] = []


class AnyAppAccessPipline(Pipeline):
    routes_confs: List[PipelinedRouteConf] = []


@mark_pipelined(AnyAppPipeline)
class AnyService(Service):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = "asgajsdhbngaksngkp;amsg"

    async def test(self, msg: TaskIMessage):
        await asyncio.sleep(1)
        logger.warning(self.q)
        logger.warning(msg.args)

    @set_to_pipline("/test/<id:int>", HTTPMethod.GET, AnyAppPipeline)
    async def person_details(self, inc: InputContext, prot: ProtectIdentity):
        # logger.info(inc.r_attrs)
        # logger.warning(inc.channel)
        # logger.warning(inc.named_ctx.get_obj(AnyService))
        await inc.channel.produce(TaskIMessage("test_app_task_executor", self.test, args=("asfasf",)))
        return {}


@mark_pipelined(AnyAppAccessPipline)
class OverrideUserAccess(Service):
    @set_to_pipline("/user/<entity_id:int>", HTTPMethod.GET, AnyAppAccessPipline)
    async def test(self, inc: InputContext, prot: ProtectIdentity):
        """
        test of override accesses
        :param inc:
        :param prot:
        :return:
        """
        return {}


class AnyModel(AbstractDbModel):
    pass


async def main():
    app = App("test_app", debug=True)
    app.load_config(pathlib.Path("./config.json"), AppConfg)
    sock = WebServer.create_socket(app.config.server)

    class Ansss(PDModel):
        pass

    acc = AccessService()
    map = [
        AccessSpec("/user", {HTTPMethod.GET, HTTPMethod.POST}, Protector, AnyModel, Ansss, Ansss),
        AccessSpec("/customer",
                   {HTTPMethod.GET, HTTPMethod.POST}, Protector, AnyModel, Ansss, Ansss)
    ]
    acc.add_default_routes(map, AnyAppAccessPipline)
    app.add_service(acc)
    app.add_service(OverrideUserAccess())
    # app.add_service(acc)

    # bg_wr = BGWorker("bg_worker")
    # app.add_isolate(bg_wr)
    # for i in range(os.cpu_count()):
    #     web_server = WebIsolate(f"{app.name}_sanic_{i}", app.config.server, sock)
    #     web_server.apply_named_ctx(app.ctx)
    #     app.add_isolate(web_server)
    web_server = WebServer(app.config.server)
    web_server.configure(f"{app.name}_sanic_{1}", app.ctx, sock)
    task = TaskExecutor()
    task.configure(f"{app.name}_task_executor", "something")
    web_server.add_pipelines(AnyAppPipeline)
    web_server.add_pipelines(AnyAppAccessPipline)
    app.add_isolate(web_server)
    app.add_isolate(task)
    distrib = IDistributor(app.isolates)

    def sig_handler(signal, frame):
        logger.info("Received signal %s. Shutting down.", Signals(signal).name)
        for i in app.isolates:
            i.process.terminate()
        sock.close()

    signal_func(SIGINT, lambda s, f: sig_handler(s, f))
    signal_func(SIGTERM, lambda s, f: sig_handler(s, f))

    await asyncio.wait(app.perform() + distrib.preform())

    # sock.close()

    # signal_func(SIGBREAK, lambda s, f: sig_handler(s, f))


if __name__ == '__main__':
    asyncio.run(main())
