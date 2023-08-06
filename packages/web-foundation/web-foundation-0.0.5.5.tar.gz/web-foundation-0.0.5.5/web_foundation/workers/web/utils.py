from typing import Type

from sanic import Request
from pydantic import ValidationError as PdValidationError, BaseModel as PdModel
from .erorrs.application import InconsistencyError


def validate_dto(request: Request, dto_cls: Type[PdModel]) -> PdModel:
    try:
        dto = dto_cls(**request.json)
        return dto
    except PdValidationError as ex:
        raise InconsistencyError(message=dto_validation_error_format(ex))


def dto_validation_error_format(exeption: PdValidationError):
    failed_fields = exeption.errors()
    commment_str = "Some of essential params failed : " + ", ".join(
        [str(field["loc"][-1]) + " - " + field["msg"] for field in failed_fields])
    return commment_str
