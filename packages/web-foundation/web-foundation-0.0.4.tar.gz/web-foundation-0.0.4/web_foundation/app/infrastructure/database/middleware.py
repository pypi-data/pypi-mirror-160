from typing import List, Union, TypeVar, Type, Tuple

from pydantic import BaseModel as PdModel
from tortoise.exceptions import IntegrityError, FieldError
from tortoise.queryset import QuerySetSingle, QuerySet
from web_foundation.app.infrastructure.database.models import AbstractDbModel
from web_foundation.app.infrastructure.database.utils import integrity_error_format
from web_foundation.workers.web.erorrs.application import InconsistencyError
from web_foundation.workers.web.sanic_ext.structs import ProtectIdentity

EntityId = TypeVar("EntityId", bound=int)
TypeDbModel = TypeVar("TypeDbModel", bound=AbstractDbModel)


class DatabaseMiddleware:
    pass


class RelateDMW(DatabaseMiddleware):
    @staticmethod
    async def fetch_related(model: TypeDbModel, query: Union[QuerySet, QuerySetSingle], fetch_fields: List[str]):
        if fetch_fields:
            for_select = {field for fk_field in model._meta.fk_fields for field in fetch_fields if
                          fk_field == field}
            for_prefetch = set(fetch_fields) - for_select
            if for_select:
                query = query.select_related(*for_select)
            if for_prefetch:
                query = query.prefetch_related(*for_prefetch)
        return query


class AccessDMW(DatabaseMiddleware):
    async def get_entity(self, model: Type[TypeDbModel], user, entity_id: EntityId) -> TypeDbModel: # TODO TYPED USER
        if "user" in model._meta.fields:
            entity = await model.get_or_none(id=entity_id, user_id=user.id)
        else:
            entity = await model.get_or_none(id=entity_id)
        if not entity:
            raise InconsistencyError(message=f"{model.__name__} not found")
        return entity

    @staticmethod
    async def create(model: TypeDbModel, protection: ProtectIdentity, dto: PdModel, **kwargs) -> TypeDbModel:
        entity_kwargs = {field: value for field, value in dto.dict().items() if not value is None}
        if "user" in model._meta.fields:
            entity_kwargs["user"] = protection.user
        try:
            entity = await model.create(**entity_kwargs)
        except IntegrityError as exception:
            raise integrity_error_format(exception)
        except ValueError as exception:
            raise InconsistencyError(exception)
        return entity

    @staticmethod
    async def read(model: TypeDbModel, protection: ProtectIdentity, fetch_fields: List[str] = None, **kwargs) -> \
            Union[
                TypeDbModel, None]:
        query = model.filter(id=protection.entity_id)
        if kwargs:
            query = query.filter(**kwargs)
        query = await RelateDMW.fetch_related(model, query, fetch_fields)
        entity = await query.first()
        return entity

    @staticmethod
    async def read_all(model: TypeDbModel, protection: ProtectIdentity, limit: int = None, offset: int = None,
                       fetch_fields: List[str] = None,
                       **kwargs) -> Union[Tuple[List[TypeDbModel], int], TypeDbModel]:
        query = model.filter()
        if "banned" in model._meta.fields:
            query = query.filter(banned=False)
        if kwargs:
            if "order_by" in kwargs:
                query = query.order_by(kwargs.pop("order_by"))
            query = query.filter(**kwargs)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        query = await RelateDMW.fetch_related(model, query, fetch_fields)
        try:
            entities = await query
            query._limit = None
            total = await query.count()
        except FieldError:
            raise InconsistencyError(message="Incorrect filter")
        return entities, total

    @staticmethod
    async def update(model: TypeDbModel, protection: ProtectIdentity, dto: PdModel, **kwargs) -> TypeDbModel:
        entity = await AccessDMW.get_entity(model, protection.user, protection.entity_id)
        entity_kwargs = {field: value for field, value in dto.dict().items() if value is not None}
        for field, value in entity_kwargs.items():
            setattr(entity, field, value)
        try:
            await entity.save(update_fields=list(entity_kwargs.keys()))
        except IntegrityError as exception:
            integrity_error_format(exception)
        except ValueError as exception:
            raise InconsistencyError(exception)
        return entity

    @staticmethod
    async def delete(model: TypeDbModel, protection: ProtectIdentity, **kwargs) -> TypeDbModel:
        entity = await AccessDMW.get_entity(model, protection.user, protection.entity_id)
        await entity.delete()
        return entity
