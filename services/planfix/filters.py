from enum import IntEnum
from typing import Any, TypeAlias

from pydantic import PositiveInt

from services.planfix.api.rest.enums import SubscriptionStatus
from services.planfix.api.rest.filters import CustF, FilterTypes


class CustomFields(IntEnum):
    VPN_KEY = 140146
    GUID = 140262
    REBILL_ID = 140258
    CLIENT_ID = 140264
    SUBSCRIPTION_STATUS_ID = 140268
    ACCOUNT_TOKEN = 140280
    REQUEST_KEY = 140282
    TELEGRAM_ID = 140308
    VPN_KEY_LINK = 140352
    PAYMENT_SUM = 149932
    PAYMENT_SUM2 = 140326
    USER_KEY = 139978


class VPNKeyF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_LINE
    field: PositiveInt = CustomFields.VPN_KEY


class VPNKeyLinkF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_LINE
    field: PositiveInt = CustomFields.VPN_KEY_LINK


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


class TelegramIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.TELEGRAM_ID


class SubscriptionStatusF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.SUBSCRIPTION_STATUS_ID


class PaymentSumF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.PAYMENT_SUM


class PaymentSum2F(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.PAYMENT_SUM2


class UserKeyF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.USER_KEY


CustomFieldUpdateBody: TypeAlias = dict[str, str | int | dict[str, CustomFields]]
CustomCompositeFieldUpdateBody: TypeAlias = dict[str, dict[str, CustomFields] | dict[str, Any]]


def TelegramIdUpdate(value: str | int) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.TELEGRAM_ID}, "value": value}


def RebillIdUpdate(value: str | int) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.REBILL_ID}, "value": value}


def AccountTokenUpdate(value: str) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.ACCOUNT_TOKEN}, "value": value}


def RequestKeyUpdate(value: str) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.REQUEST_KEY}, "value": value}


def SubscriptionStatusUpdate(status: SubscriptionStatus) -> CustomCompositeFieldUpdateBody:
    return {"field": {"id": CustomFields.SUBSCRIPTION_STATUS_ID}, "value": {"id": status}}


def PaymentSumUpdate(value: int) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.PAYMENT_SUM}, "value": value}


def PaymentSum2Update(value: int) -> CustomFieldUpdateBody:
    return {"field": {"id": CustomFields.PAYMENT_SUM2}, "value": value}


def UserKeyUpdate(value: int) -> CustomCompositeFieldUpdateBody:
    return {"field": {"id": CustomFields.USER_KEY}, "value": {"id": value}}
