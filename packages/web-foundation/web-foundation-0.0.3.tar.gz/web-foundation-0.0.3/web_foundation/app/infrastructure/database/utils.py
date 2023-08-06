from datetime import datetime
from datetime import date as Ddate
from datetime import time as DTime


def string_from_db_date(db_date: datetime | Ddate | DTime, iso_date_format=False):
    v = db_date
    if isinstance(db_date, datetime):
        if iso_date_format:
            v = db_date.replace(microsecond=0).astimezone().isoformat()
        else:
            v = db_date.astimezone().strftime("%d.%m.%Y, %H:%M:%S %z")
    elif isinstance(db_date, Ddate):
        if iso_date_format:
            v = db_date.isoformat()
        else:
            v = db_date.strftime("%d.%m.%Y")
    elif isinstance(db_date, DTime):
        v = db_date.replace(microsecond=0).isoformat()
    return v


def integrity_error_format(exception) -> str:
    str_exception = str(exception)
    if "table" in str_exception:
        # tortoise.exceptions.IntegrityError: insert or update on table "issue"
        # violates foreign key constraint "issue_service_id_fkey"
        start_tablename = str_exception.rfind("table") + 7
        end_tablename = str_exception.rfind(".", start_tablename) - 1
        return f"Related model {str_exception[start_tablename:end_tablename].capitalize()} not exist"
    elif str_exception.startswith("null"):
        start_field_name = str_exception.find('"') + 1
        end_field_name = str_exception.rfind('"')
        return f"{str_exception[start_field_name:end_field_name]} can't be null"
    else:
        return str(exception)
