from dataclasses import dataclass, field
from enum import Enum
from types import SimpleNamespace
from typing import Dict

from pydantic import BaseModel as PdModel
from sanic import Request

from web_foundation.kernel import NamedContext
from web_foundation.kernel.isolates.channel import IChannel


@dataclass
class ProtectIdentity:
    pass


@dataclass
class InputContext:
    r_args: SimpleNamespace
    r_kwargs: Dict
    named_ctx: NamedContext
    channel: IChannel
    dto: PdModel | None
    request: Request


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"

    @staticmethod
    def all():
        return [HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PATCH, HTTPMethod.DELETE]
