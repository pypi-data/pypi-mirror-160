from dataclasses import dataclass
from functools import partial, wraps
from typing import List, Set, Type
import json as py_json
from pydantic import BaseModel as PdModel
from sanic import json
from sanic.exceptions import NotFound

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
                match method:
                    case HTTPMethod.GET:
                        r = set_to_pipline(acc.uri,
                                           method,
                                           pipline,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                        r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                           method,
                                           pipline,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.POST:
                        r = set_to_pipline(acc.uri,
                                           method,
                                           pipline,
                                           struct=acc.create_struct,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.PATCH:
                        r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                           method,
                                           pipline,
                                           struct=acc.update_struct,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access, model=acc.model)))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.DELETE:
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
                kwargs = inc.r_kwargs
                if inc.r_args.entity_id is None:
                    limit = inc.request.args.get("limit")
                    offset = inc.request.args.get("offset")
                    limit = int(limit) if limit and limit.isdigit() else 100
                    offset = int(offset) if offset and offset.isdigit() else None

                    for ar, val in inc.request.args.items():
                        if ar in ["limit", "offset"]:
                            continue
                        val = val[0]
                        if val.lower() == 'false':
                            val = False
                        elif val.lower() == 'true':
                            val = True
                        elif val.isdigit():
                            val = int(val)
                        elif "." in val and val.replace('.', '').isdigit():
                            val = float(val)
                        elif val.startswith("["):
                            val = py_json.loads(val)
                        kwargs[ar] = val

                    models = await AccessDMW.read_all(model, prot, limit, offset, **kwargs)
                    result = [await model.values_dict() for model in models]
                    return json(result)
                model = await AccessDMW.read(model, prot, **kwargs)
                if model:
                    result = await model.values_dict()
                    return json(result)
                else:
                    raise NotFound()
            case HTTPMethod.POST.value:
                model = await AccessDMW.create(model, prot, inc.dto)
                if isinstance(model, list):
                    return json([await i.values_dict() for i in model])
                return json(await model.values_dict())
            case HTTPMethod.PATCH.value:
                model = await AccessDMW.update(model, prot, inc.dto)
                return json(await model.values_dict())
            case HTTPMethod.DELETE.value:
                result = await AccessDMW.delete(model, prot)
                if isinstance(result, int):
                    return json(result)
                return json(await result.values_dict())
