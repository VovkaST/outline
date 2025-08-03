from enum import IntEnum

from pydantic import PositiveInt

from app_server.services.planfix.api.rest.enums import SubscriptionStatus
from app_server.services.planfix.api.rest.filters import CustF, FilterTypes


class CustomFields(IntEnum):
    GUID = 140262
    REBILL_ID = 140258
    CLIENT_ID = 140264
    SUBSCRIPTION_STATUS_ID = 140268
    ACCOUNT_TOKEN = 140280
    REQUEST_KEY = 140282
    PAYMENT_SUM = 149932


class GuidF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_LINE
    field: PositiveInt = CustomFields.GUID


class RebillIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.REBILL_ID


class ClientIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.CLIENT_ID


class RequestKeyF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.REQUEST_KEY


class SubscriptionStatusF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.SUBSCRIPTION_STATUS_ID


class PaymentSumF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.PAYMENT_SUM


def RebillIdUpdate(value: str | int) -> dict:
    return {"field": {"id": CustomFields.REBILL_ID}, "value": value}


def AccountTokenUpdate(value: str) -> dict:
    return {"field": {"id": CustomFields.ACCOUNT_TOKEN}, "value": value}


def RequestKeyUpdate(value: str) -> dict:
    return {"field": {"id": CustomFields.REQUEST_KEY}, "value": value}


def SubscriptionStatusUpdate(status: SubscriptionStatus) -> dict:
    return {"field": {"id": CustomFields.SUBSCRIPTION_STATUS_ID}, "value": {"id": status}}


def PaymentSumUpdate(value: int) -> dict:
    return {"field": {"id": CustomFields.PAYMENT_SUM}, "value": value}
