import sys
from types import MethodType
from typing import Type

import loguru

from .namespace import Obj


def class_of_method(method: MethodType) -> Type[Obj]:
    # return method.__self__
    return vars(sys.modules[method.__module__])[method.__qualname__.split('.')[0]]
