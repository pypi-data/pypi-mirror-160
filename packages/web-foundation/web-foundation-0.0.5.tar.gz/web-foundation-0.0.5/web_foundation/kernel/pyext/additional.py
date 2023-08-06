import sys
from types import MethodType
from typing import Type, Callable, Any

import loguru
from mypy_extensions import VarArg, KwArg

from .namespace import Obj


def class_of_method(method: Callable[[VarArg(Any), KwArg(Any)], Any]) -> Type[Obj]:
    # return method.__self__
    return vars(sys.modules[method.__module__])[method.__qualname__.split('.')[0]]
