from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, PositiveInt, computed_field
from typing_extensions import Self

from services.planfix.api.rest.enums import OrderDirection, Role, TypeList
from services.planfix.api.rest.filters import CustF, F
from services.planfix.api.rest.responses import ObjectId


class BaseRequest(BaseModel):
    _fields: list[str] = []

    @computed_field
    @property
    def fields(self) -> str:
        field_names = [str(f.field.value) if isinstance(f, CustF) else f.type.label for f in self.filters]
        return ",".join(list(self._fields) + field_names)

    def with_fields(self, *fields: list[str]) -> Self:
        instance = self.model_copy(deep=True)
        cleared_list = []
        for field in fields:
            if field not in self._fields:
                cleared_list.append(str(field))
        instance._fields = cleared_list
        return instance


class BaseEntity(BaseModel):
    id: ObjectId | None = None
    name: str | None = None


class _TimePoint(BaseModel):
    date: str = Field(examples=["01-12-1900 (dd-MM-yyyy)"])
    time: str = Field(examples=["00:00 (HH:mm)"])
    datetime: str = Field(title="By ISO format", examples=["1900-12-01T00:00Z (yyyy-MM-dd'T'HH:mm'Z')"])


class _PersonRequest(BaseModel):
    id: str


class _GroupRequest(BaseModel):
    id: str


class ResultOrder(BaseModel):
    field: str
    direction: OrderDirection = OrderDirection.ASC


class Filter(BaseRequest):
    offset: PositiveInt | None = 0
    pageSize: PositiveInt | None = 100
    filters: list[CustF | F] | None = Field(default_factory=list)


class CommentsFilter(Filter):
    typeList: TypeList = TypeList.COMMENTS
    resultOrder: list[ResultOrder] = Field(default_factory=[])


class _PeopleRequest(BaseModel):
    users: list[_PersonRequest] = Field(default_factory=list)
    groups: list[_GroupRequest] = Field(default_factory=list)
    roles: list[Role] = Field(default_factory=list)


class AddComment(BaseModel):
    sourceId: str | None = None
    sourceObjectId: str | None = None
    sourceDataVersion: str | None = None
    dateTime: _TimePoint | None = Field(default_factory=dict)
    description: str | None = None
    owner: _PersonRequest | None = Field(default_factory=dict)
    isPinned: bool = False
    isHidden: bool = False
    recipients: _PeopleRequest | None = Field(default_factory=dict)


class CustomFieldValueRequest(BaseModel):
    field: BaseEntity | None = Field(default_factory=BaseEntity)
    value: Any | None = None


class TaskCreateRequest(BaseModel):
    name: str
    description: str | None = Field(default=None)
    customFieldData: list[CustomFieldValueRequest] | None = Field(default_factory=list)


class TaskCreateByTemplateRequest(TaskCreateRequest):
    class Template(BaseModel):
        id: int

    template: Template


class TaskCreateWithSetFieldRequest(TaskCreateByTemplateRequest):
    customFieldData: list[CustomFieldValueRequest] | None = Field(default_factory=list)


class TaskUpdateRequest(BaseModel):
    customFieldData: list[CustomFieldValueRequest] | None = Field(default_factory=list)
