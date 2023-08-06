from dataclasses import dataclass
from functools import partial, wraps
from typing import List, Set, Type

from pydantic import BaseModel as PdModel

from web_foundation.app.infrastructure.database.middleware import AccessDMW
from web_foundation.app.infrastructure.database.models import AbstractDbModel
from web_foundation.app.service.service import Service
from web_foundation.workers.web.sanic_ext.pipline_ext import set_to_pipline, Protector, Pipeline, mark_pipelined
from web_foundation.workers.web.sanic_ext.structs import HTTPMethod, ProtectIdentity, InputContext


@dataclass
class AccessSpec:
    uri: str
    methods: Set[HTTPMethod]
    protector: Type[Protector] | None
    model: Type[AbstractDbModel]
    create_struct: Type[PdModel] | None
    update_struct: Type[PdModel] | None


class AccessService(Service):
    def add_default_routes(self, access_mapping: List[AccessSpec], pipline: Type[Pipeline]):
        for acc in access_mapping:
            for method in acc.methods:
                if method not in [HTTPMethod.DELETE, HTTPMethod.PATCH]:
                    r = set_to_pipline(acc.uri,
                                       method,
                                       pipline,
                                       protector=acc.protector)(
                        wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                    setattr(AccessService.exec_access, "route_conf", r.route_conf)
                    mark_pipelined(pipline)(AccessService)
                if method in [HTTPMethod.DELETE, HTTPMethod.PATCH, HTTPMethod.GET]:
                    r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                       method,
                                       pipline,
                                       protector=acc.protector)(
                        wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                    setattr(AccessService.exec_access, "route_conf", r.route_conf)
                    mark_pipelined(pipline)(AccessService)

    async def exec_access(self, inc: InputContext, prot: ProtectIdentity, model: AbstractDbModel = None):
        """
        Access to models
        :param inc:
        :param prot:
        :param model:
        :return:
        """
        if not model:
            raise AttributeError(f"exec_access must have model kwarg")
        match inc.request.method:
            case HTTPMethod.GET.value:
                return await AccessDMW.read(model, prot, inc.dto)
            case HTTPMethod.POST.value:
                return await AccessDMW.create(model, prot, inc.dto)
            case HTTPMethod.PATCH.value:
                return await AccessDMW.update(model, prot, inc.dto)
            case HTTPMethod.DELETE.value:
                return await AccessDMW.delete(model, prot, inc.dto)
