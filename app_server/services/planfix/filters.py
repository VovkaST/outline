from enum import IntEnum

from pydantic import PositiveInt

from app_server.services.planfix.api.rest.filters import CustF, FilterTypes


class CustomFields(IntEnum):
    GUID = 140262
    REBILL_ID = 140258


class GuidF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_LINE
    field: PositiveInt = CustomFields.GUID


class RebillIdF(CustF):
    type: FilterTypes = FilterTypes.CUSTOM_FIELD_NUMBER
    field: PositiveInt = CustomFields.REBILL_ID
