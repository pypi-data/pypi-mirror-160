from typing import List, Union

from pydantic import BaseModel as PdModel
from tortoise.queryset import QuerySetSingle, QuerySet

from web_foundation.app.infrastructure.database.models import AbstractDbModel
from web_foundation.workers.web.sanic_ext.structs import ProtectIdentity


class DatabaseMiddleware:
    pass


class RelateDMW(DatabaseMiddleware):
    @staticmethod
    async def fetch_related(model: AbstractDbModel, query: Union[QuerySet, QuerySetSingle], fetch_fields: List[str]):
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
    # async def _get_entity(self, user: Union[User, Admin], entity_id: EntityId) -> AbstractBaseModel:
    #     if "user" in self.target_model._meta.fields:
    #         entity = await self.target_model.get_or_none(id=entity_id, user_id=user.id)
    #     else:
    #         entity = await self.target_model.get_or_none(id=entity_id)
    #     if not entity:
    #         raise NotFound(message=f"{self.target_model.__name__} with id={entity_id} not found")
    #         # raise InconsistencyError(message=f"{self.target_model.__name__} not found")
    #     return entity
    @staticmethod
    async def create(model: AbstractDbModel, protection: ProtectIdentity, dto: PdModel, **kwargs) -> AbstractDbModel:
        return {}
        pass
        # entity_kwargs = {field: value for field, value in _dto.dict().items() if not value is None}
        # if "user" in self.target_model._meta.fields:
        #     entity_kwargs["user"] = user
        # try:
        #     entity = await self.target_model.create(**entity_kwargs)
        # except IntegrityError as exception:
        #     raise integrity_error_format(exception)
        # except ValueError as exception:
        #     raise InconsistencyError(exception)
        # return entity

    @staticmethod
    async def read(model: AbstractDbModel, protection: ProtectIdentity, fetch_fields: List[str] = None, **kwargs) -> \
            Union[
                AbstractDbModel, None]:
        return {}
        pass
        # query = self.target_model.filter(id=entity_id)
        # if kwargs:
        #     query = query.filter(**kwargs)
        # query = await self._fetch_related(query, fetch_fields)
        # entity = await query.first()
        # return entity

    #
    # async def read_all(self,protection: ProtectionIdentity, limit: int = None, offset: int = None, fetch_fields: List[str] = None,
    #                    **kwargs) -> Union[Tuple[List[AbstractBaseModel], int], AbstractBaseModel]:
    #     query = self.target_model.filter()
    #
    #     # if "user" in self.target_model._meta.fields:
    #     #     query = query.filter(user_id=user.id)
    #     if "banned" in self.target_model._meta.fields:
    #         query = query.filter(banned=False)
    #     if kwargs:
    #         if "order_by" in kwargs:
    #             query = query.order_by(kwargs.pop("order_by"))
    #         query = query.filter(**kwargs)
    #
    #     if limit:
    #         query = query.limit(limit)
    #     if offset:
    #         query = query.offset(offset)
    #     query = await self._fetch_related(query, fetch_fields)
    #     try:
    #         entities = await query
    #         query._limit = None
    #         total = await query.count()
    #     except FieldError:
    #         raise InconsistencyError(message="Incorrect filter")
    #     return entities, total
    @staticmethod
    async def update(model: AbstractDbModel, protection: ProtectIdentity, dto: PdModel, **kwargs) -> AbstractDbModel:
        return {}
        pass
        # entity = await self._get_entity(user, entity_id)
        # entity_kwargs = {field: value for field, value in dto.dict().items() if value is not None}
        # for field, value in entity_kwargs.items():
        #     setattr(entity, field, value)
        # try:
        #     await entity.save(update_fields=list(entity_kwargs.keys()))
        # except IntegrityError as exception:
        #     integrity_error_format(exception)
        # except ValueError as exception:
        #     raise InconsistencyError(exception)
        # return entity

    @staticmethod
    async def delete(model: AbstractDbModel, protection: ProtectIdentity, dto: PdModel, **kwargs) -> AbstractDbModel:
        return {}
        pass
        # entity = await self._get_entity(user, entity_id)
        # await entity.delete()
        # return entity
