from typing import Type, TypeVar, Dict

from web_foundation.kernel.pyext.namespace import Obj, IterableNamespace, TypedNamespace
from web_foundation.kernel.pyext.named_obj import NamedObject


class NamedContext(IterableNamespace):
    _CtxKind = TypeVar("_CtxKind")
    _spaces: Dict[_CtxKind, TypedNamespace]
    _founded_obj: Dict[Type[NamedObject], NamedObject]

    class NotFindInContext(Exception):
        pass

    class DefaultKind:
        pass

    def __init__(self):
        super(NamedContext, self).__init__()
        self._spaces = {}
        self._founded_obj = {}
        self._spaces.update({self.DefaultKind: TypedNamespace()})

    def get_obj(self, obj_type: Type[Obj]) -> NamedObject:
        if obj_type in self._founded_obj:
            return self._founded_obj.get(obj_type)
        obj = None
        for kind, space in self._spaces.items():
            try:
                obj = space.get_(obj_type)
            except AttributeError as e:
                pass
        if not obj:
            raise self.NotFindInContext(f"Obj type {obj_type} not found in all kinds in context")
        self._founded_obj.update({obj_type: obj})
        return obj

    def set_obj(self, obj: NamedObject, kind: _CtxKind = DefaultKind) -> None:
        if kind not in self._spaces:
            self._spaces.update({kind: TypedNamespace()})
        self._spaces[kind].set_(obj)
