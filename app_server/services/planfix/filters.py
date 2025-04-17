from enum import IntEnum

from pydantic import PositiveInt

from app_server.services.planfix.api.rest.enums import SubscriptionStatus
from app_server.services.planfix.api.rest.filters import CustF, FilterTypes


class CustomFields(IntEnum):
    GUID = 140262
    REBILL_ID = 140258
    CLIENT_ID = 140264
    SUBSCRIPTION_STATUS_ID = 140268


class GuidF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_LINE
    field: PositiveInt = CustomFields.GUID


class RebillIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.REBILL_ID


class ClientIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.CLIENT_ID


class SubscriptionStatusF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.SUBSCRIPTION_STATUS_ID


def SubscriptionStatusUpdate(status: SubscriptionStatus) -> dict:
    return {"field": {"id": CustomFields.SUBSCRIPTION_STATUS_ID}, "value": {"id": status}}
