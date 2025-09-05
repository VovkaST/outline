from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, PositiveInt, field_serializer


class OperatorTypes(str, Enum):
    EQUAL = "equal"


class FilterTypes(Enum):
    ASSIGNER = 1, "assigner"
    ASSIGNEES = 2, "assignees"
    AUDITORS = 3, "auditors"
    PROJECT = 5, "project"
    COUNTERPARTY = 7, "counterparty"
    PRIORITY = 9, "priority"
    STATUS = 10, "status"
    START_DATE = 13, "startDateTime"
    END_DATE = 14, "endDateTime"
    PROCESS_ID = 24, "processId"
    START_DATE_TYME = 25, "startDateTime"
    TEMPLATE = 51, "template"
    OBJECT = 51, "object"
    NUMBER = 57, "number"
    DATA_TAG = 93, "dataTags"
    CUSTOM_FIELD_LINE = 101, "87"
    CUSTOM_FIELD_NUMBER = 102, "5"
    CUSTOM_FIELD_DATE = 103, "88"
    CUSTOM_FIELD_CHECKBOX = 105, "97"
    CUSTOM_FIELD_LIST = 106, "11"
    CUSTOM_FIELD_DIRECTORY_ENTRY = 107, "20"
    CUSTOM_FIELD_CONTACT = 108, "87"
    CUSTOM_FIELD_EMPLOYEE = 109, "87"
    CUSTOM_FIELD_COUNTERPARTY = 110, "5"
    CUSTOM_FIELD_GRP_EMP_CONT = 112, "96"
    CUSTOM_FIELD_LIST_OF_USERS = 113, "15"
    CUSTOM_FIELD_SET_OF_DIRECTORY_VALUES = 114, "21"
    CUSTOM_FIELD_TASK = 115, "50"
    CUSTOM_FIELD_PROJECT = 117, "50"

    def __init__(self, code, label):
        self.code = code
        self.label = label

    def value(self) -> int:
        return self.code


class F(BaseModel):
    type: FilterTypes
    operator: OperatorTypes = OperatorTypes.EQUAL
    value: Any

    @field_serializer("type")
    def serialize_type(self, type: FilterTypes, _info) -> int:
        return type.code


class CustF(F):
    field: PositiveInt
