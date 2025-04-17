from __future__ import annotations

from contextlib import suppress
from datetime import datetime

from app_server.services.planfix.api.rest.responses import CustomFieldValueResponse
from app_server.services.planfix.filters import CustomFields
from root.config import settings


def get_custom_field(field: CustomFields, field_values: list[CustomFieldValueResponse]) -> CustomFieldValueResponse:
    with suppress(StopIteration):
        return next(filter(lambda d: d.field.id == field, field_values))


def get_rebill_field(fields: list[CustomFieldValueResponse]) -> CustomFieldValueResponse:
    return get_custom_field(field=CustomFields.REBILL_ID, field_values=fields)


def make_order_uniq_id(task_guid: str) -> str:
    suffix = datetime.now().strftime("%y%m%d_%H%M")
    return f"{task_guid}.{suffix}"


def build_success_url(task_guid: str) -> str:
    return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=true"
