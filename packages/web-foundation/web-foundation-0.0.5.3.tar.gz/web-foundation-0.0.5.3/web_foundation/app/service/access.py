from dataclasses import dataclass, field
from functools import partial, wraps
from typing import List, Set, Type, Generic, Protocol
import json as py_json
from pydantic import BaseModel as PdModel
from sanic import json
from sanic.exceptions import NotFound

from web_foundation.app.infrastructure.database.middleware import AccessDMW, AccessProtectIdentity, \
    EntityId  # type: ignore
from web_foundation.app.infrastructure.database.models import AbstractDbModel, GenericDbType
from web_foundation.app.service.service import Service
from web_foundation.workers.web.sanic_ext.pipline_ext import set_to_pipline, Protector, Pipeline, mark_pipelined
from web_foundation.workers.web.sanic_ext.structs import HTTPMethod, ProtectIdentity, InputContext


@dataclass
class AccessSpec(Generic[GenericDbType]):
    uri: str
    methods: Set[HTTPMethod]
    model: GenericDbType
    protector: Type[Protector] | None = field(default=None)
    create_struct: Type[PdModel] | None = field(default=None)
    update_struct: Type[PdModel] | None = field(default=None)


class AccessService(Service):

    def add_default_routes(self, access_mapping: List[AccessSpec], pipline: Type[Pipeline],
                           access_middleware: AccessDMW | None = None):
        db_middleware = access_middleware if access_middleware else AccessDMW
        for acc in access_mapping:
            for method in acc.methods:
                match method:
                    case HTTPMethod.GET:
                        r = set_to_pipline(acc.uri,
                                           method,
                                           pipline,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access,
                                                                     model=acc.model,
                                                                     access_middleware=db_middleware
                                                                     )))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                        r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                           method,
                                           pipline,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access,
                                                                     model=acc.model,
                                                                     access_middleware=db_middleware
                                                                     )))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.POST:
                        r = set_to_pipline(acc.uri,
                                           method,
                                           pipline,
                                           struct=acc.create_struct,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access,
                                                                     model=acc.model,
                                                                     access_middleware=db_middleware
                                                                     )))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.PATCH:
                        r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                           method,
                                           pipline,
                                           struct=acc.update_struct,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access,
                                                                     model=acc.model,
                                                                     access_middleware=db_middleware
                                                                     )))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)
                    case HTTPMethod.DELETE:
                        r = set_to_pipline(acc.uri + "/<entity_id:int>",
                                           method,
                                           pipline,
                                           protector=acc.protector)(
                            wraps(AccessService.exec_access)(partial(AccessService.exec_access,
                                                                     model=acc.model,
                                                                     access_middleware=db_middleware
                                                                     )))
                        setattr(AccessService.exec_access, "route_conf", r.route_conf)
                        mark_pipelined(pipline)(AccessService)

    async def exec_access(self,
                          inc: InputContext,
                          prot: AccessProtectIdentity,
                          model: AbstractDbModel,
                          access_middleware: AccessDMW
                          ):
        """
        Access to models
        :param inc:
        :param prot:
        :param model:
        :return:
        """
        match inc.request.method:
            case HTTPMethod.GET.value:
                kwargs = inc.r_kwargs
                entity_id = kwargs.get("entity_id")
                if entity_id is None:
                    limit = inc.request.args.get("limit")
                    offset = inc.request.args.get("offset")
                    limit = int(limit) if limit and limit.isdigit() else 100
                    offset = int(offset) if offset and offset.isdigit() else None
                    # order_by = inc.request.args.get("order_by")  # for openapi. Variable forwarded to read_all in kwargs
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

                    retrieved_all, total = await access_middleware.read_all(model, prot, limit, offset, **kwargs)
                    res = [await model.values_dict() for model in retrieved_all]
                    return res
                retrieved = await access_middleware.read(model, entity_id, prot, **kwargs)
                if retrieved:
                    result = await retrieved.values_dict()
                    return result
                else:
                    raise NotFound()

            case HTTPMethod.POST.value:
                assert inc.dto
                retrieved = await access_middleware.create(model, prot, inc.dto, **inc.r_kwargs)
                if isinstance(retrieved, list):
                    return json([await i.values_dict() for i in retrieved])
                return json(await retrieved.values_dict())

            case HTTPMethod.PATCH.value:
                assert inc.dto
                entity_id = inc.r_kwargs.get("entity_id")
                assert entity_id
                retrieved = await access_middleware.update(model, entity_id, prot, inc.dto, **inc.r_kwargs)
                return json(await retrieved.values_dict())

            case HTTPMethod.DELETE.value:
                entity_id = inc.r_kwargs.get("entity_id")
                assert entity_id
                retrieved = await access_middleware.delete(model, entity_id, prot, **inc.r_kwargs)
                return json(await retrieved.values_dict())
