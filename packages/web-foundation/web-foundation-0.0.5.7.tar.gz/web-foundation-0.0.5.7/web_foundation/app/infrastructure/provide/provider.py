from __future__ import annotations

from typing import Dict, Type, TypeVar, Generic

T = TypeVar("T")


class Provider(Generic[T]):
    provided_entities: Dict[str, Dict[Type[T], T]] = {}

    @staticmethod
    def reg(app_name: str, initiator):
        Provider.provided_entities.update({app_name: {type(initiator): initiator}})  # type: ignore

    @staticmethod
    def of(initiator_type: Type[T], app_name: str) -> T:
        if not Provider.provided_entities.get(app_name):  # type: ignore
            raise ValueError(f"App {app_name} not found in provide context")
        if not Provider.provided_entities.get(app_name).get(initiator_type):  # type: ignore
            raise ValueError(f"Provider {initiator_type.__name__} for {app_name} not found in provide context")
        return Provider.provided_entities.get(app_name).get(initiator_type)  # type: ignore
