from types import SimpleNamespace
from typing import Tuple, Any, Iterator
from typing import Type, TypeVar

from web_foundation.kernel.pyext.named_obj import NamedObject

Obj = TypeVar("Obj", bound=NamedObject, covariant=True)


class IterableNamespace(SimpleNamespace):

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter((item_name, item) for item_name, item in self.__dict__.items())


class TypedNamespace(IterableNamespace):

    def __contains__(self, item: Type[NamedObject]):
        return item in self.__dict__

    def get_(self, item: Type[Obj]) -> Obj:
        return self.__getattribute__(item.sname)

    def set_(self, cls: NamedObject):
        setattr(self, cls.sname, cls)
