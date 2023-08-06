import warnings
from dataclasses import dataclass
from distutils.version import LooseVersion
from functools import wraps
from http.client import HTTPResponse
from types import MethodType, SimpleNamespace
from typing import List, Any, Dict, Callable, Type

from pydantic import BaseModel as PdModel
from sanic import __version__ as sanic_version, Request, json, text

from web_foundation.kernel import class_of_method, NamedContext
from web_foundation.workers.web.sanic_ext.structs import InputContext, ProtectIdentity, HTTPMethod
from web_foundation.workers.web.utils import validate_dto

try:
    import sanic_ext
    from sanic_ext.extensions.base import Extension
    from sanic_ext.config import Config

    use_ext = True
except ImportError:
    use_ext = False
    Extension = object
    from sanic.config import Config

SANIC_VERSION = LooseVersion(sanic_version)
SANIC_21_9_0 = LooseVersion("21.9.0")


class RequestParser:
    extracted_attrs: List[str]
    struct: PdModel | None
    dto_validation_fnc: Callable[[Request, Type[PdModel]], PdModel]

    def __init__(self,
                 dto_validation_fnc: Callable[[Request, Type[PdModel]], PdModel],
                 extracted_attrs: List[str] = None,
                 struct: PdModel = None):
        self.dto_validation_fnc = dto_validation_fnc
        self.struct = struct
        if extracted_attrs:
            for attr in extracted_attrs:
                if not hasattr(Request, attr):
                    raise AttributeError(f"sanic.Request has not attribute {attr}")
        self.extracted_attrs = extracted_attrs

    def income_(self, request: Request, **kwargs) -> InputContext:
        incoming_context = InputContext(r_args=SimpleNamespace(), r_kwargs={}, named_ctx=request.app.ctx.named_ctx,
                                        dto=None, channel=request.app.ctx.channel, request=request)
        if self.extracted_attrs:
            for attr in self.extracted_attrs:
                setattr(incoming_context.r_args, attr, getattr(request, attr))
        incoming_context.r_kwargs = kwargs
        if self.struct:
            incoming_context.dto = self.dto_validation_fnc(request, self.struct)
        return incoming_context


class ResponseConstructor:
    fabric: Callable[[...], HTTPResponse]
    default_response: HTTPResponse
    pd_model: Type[PdModel]

    def __init__(self,
                 pd_model: Type[PdModel] = None,
                 fabric: Callable[[...], HTTPResponse] = None,
                 default_response: HTTPResponse = None):
        self.default_response = default_response
        self.pd_model = pd_model
        self.fabric = fabric

    def return_(self, to_response: Any) -> HTTPResponse:
        return self.fabric(to_response) if self.fabric else self.default_response


class Protector:
    named_ctx: NamedContext

    def __init__(self, named_ctx: NamedContext):
        self.named_ctx = named_ctx

    @classmethod
    async def protect(cls, request: Request) -> ProtectIdentity | None:
        return None


class AbcPipeline:
    pass


@dataclass()
class PipelinedRouteConf:
    pipeline: Type[AbcPipeline] | List[Type[AbcPipeline]] | None
    uri: str
    method: HTTPMethod
    target: MethodType
    protector: Type[Protector]
    kwargs: Dict[str, Any]

    def __eq__(self, other):
        return self.uri == other.uri and self.method == other.method

    def __str__(self):
        return f"Route-conf in pipeline {self.pipeline} to {self.uri} {self.method} on {self.target}"


class Pipeline(AbcPipeline):
    routes_confs: List[PipelinedRouteConf]

    def __str__(self):
        return ";".join(self.routes_confs)


class PipelinesExt(Extension):
    name: str = "SanicPipeline"
    _pipelines: List[Pipeline]

    def __init__(self):
        self._pipelines = []

    @property
    def pipelines(self):
        return self._pipelines

    @pipelines.setter
    def pipelines(self, value: List[Pipeline]):
        self._pipelines = value

    def startup(self, bootstrap) -> None:
        if SANIC_21_9_0 > SANIC_VERSION:
            raise RuntimeError(
                "You cannot use this version of SanicPipeline with"
                "Sanic earlier than v21.9.0")
        for pipel in self._pipelines:
            for route_cfg in pipel.routes_confs:
                try:
                    bootstrap.app.ctx.named_ctx.get_obj(class_of_method(route_cfg.target))
                except NamedContext.NotFindInContext:
                    raise AttributeError(f"Can't start unset {class_of_method(route_cfg.target)} to named context")
                bootstrap.app.add_route(route_cfg.target, route_cfg.uri, methods=[route_cfg.method.value],
                                        **route_cfg.kwargs)


def set_to_pipline(uri: str,
                   method: HTTPMethod,
                   pipline: Type[Pipeline] | List[Type[Pipeline]] | None = None,
                   protector: Type[Protector] = Protector,
                   struct: PdModel = None,
                   out_struct: PdModel = None,
                   extracted_attrs: List[str] = None,
                   dto_validation_fnc: Callable[[Request, Type[PdModel]], PdModel] = validate_dto,
                   return_fabric: Callable[[...], HTTPResponse] = json,
                   default_response: HTTPResponse = text("ok"),
                   **route_kwargs):
    def called_method(target: MethodType):
        @wraps(target)
        async def f(*args, **kwargs):
            req: Request = args[0]
            n_ctx = req.app.ctx.named_ctx
            prot_identity = await (protector(n_ctx).protect(req))
            incoming = RequestParser(dto_validation_fnc, extracted_attrs, struct).income_(req, **kwargs)
            ret_val = await target(n_ctx.get_obj(class_of_method(target)), incoming, prot_identity)
            return ResponseConstructor(out_struct, return_fabric, default_response).return_(ret_val)

        f.route_conf = PipelinedRouteConf(pipline, uri, method, f, protector, route_kwargs)
        return f

    return called_method


def mark_pipelined(*args: Type[Pipeline]):
    def wrp(cls):
        for name, method in cls.__dict__.items():
            if hasattr(method, "route_conf"):
                for pipline in args:
                    if isinstance(method.route_conf.pipeline, list):
                        for p in method.route_conf.pipeline:
                            if p == pipline and method.route_conf not in pipline.routes_confs:
                                pipline.routes_confs.append(method.route_conf)
                    elif issubclass(method.route_conf.pipeline, Pipeline):
                        if method.route_conf.pipeline == pipline and method.route_conf not in pipline.routes_confs:
                            pipline.routes_confs.append(method.route_conf)
                    else:
                        warnings.warn(f"Pipline to {method.route_conf} NOT DEFINED")
        return cls

    return wrp
