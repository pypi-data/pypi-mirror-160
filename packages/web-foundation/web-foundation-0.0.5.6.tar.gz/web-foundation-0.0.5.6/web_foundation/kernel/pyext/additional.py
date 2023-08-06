import sys
from typing import Type, Callable, Any

from .namespace import Obj


def class_of_method(method: Callable[[Any], Any]) -> Type[Obj]:
    # return method.__self__
    return vars(sys.modules[method.__module__])[method.__qualname__.split('.')[0]]
