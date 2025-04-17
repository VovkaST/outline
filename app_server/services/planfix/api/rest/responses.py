from contextlib import suppress
from functools import cached_property
from typing import TypeAlias

from pydantic import BaseModel, Field, computed_field

from app_server.services.planfix.api.rest.enums import DurationType, DurationUnit, Priority
from app_server.services.planfix.filters import CustomFields

ObjectId: TypeAlias = int | str


class BaseEntity(BaseModel):
    id: ObjectId | None = None
    name: str | None = None


class Text(BaseModel):
    lang: str | None = None
    name: str | None = None


class TimePoint(BaseModel):
    date: str | None = Field(examples=["01-12-1900 (dd-MM-yyyy)"], default=None)
    time: str | None = Field(examples=["00:00 (HH:mm)"], default=None)
    datetime: str | None = Field(
        title="By ISO format", examples=["1900-12-01T00:00Z (yyyy-MM-dd'T'HH:mm'Z')"], default=None
    )


class TaskStatus(BaseModel):
    id: ObjectId | None = None
    name: str | None = None
    color: str | None = None
    isActive: bool | None = None
    hasDeadline: bool | None = None
    isAppliedIndividually: bool | None = None
    texts: list[Text] = Field(default_factory=list)


class PersonResponse(BaseModel):
    id: ObjectId | None = None
    name: str | None = None


class GroupResponse(BaseModel):
    id: ObjectId | None = None
    name: str | None = None


class PeopleResponse(BaseModel):
    users: list[PersonResponse] | None = Field(default_factory=list)
    groups: list[GroupResponse] | None = Field(default_factory=list)


class CustomField(BaseModel):
    id: ObjectId | None = None
    name: str | None = None
    names: dict | None = Field(default_factory=dict)
    numberOfDecimalPlaces: int | None = None
    objectType: int | None = None
    type: int | None = None
    delimiter: str | None = None
    groupId: int | None = None
    directoryId: int | None = None
    directoryFields: list[int] | None = Field(default_factory=list)
    enumValues: list[str] | None = Field(default_factory=list)
    mainValue: str | None = None


class CustomFieldValueResponse(BaseModel):
    field: CustomField | None = Field(default_factory=CustomField)
    value: str | None = None
    stringValue: str | None = None


class TaskResponse(BaseModel):
    id: ObjectId
    sourceObjectId: str | None = None
    sourceDataVersion: str | None = None
    name: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: TaskStatus = Field(default_factory=TaskStatus)
    processId: int | None = None
    resultChecking: bool | None = None
    type: str | None = None
    assigner: PersonResponse = Field(default_factory=PersonResponse)
    parent: BaseEntity | None = Field(default_factory=BaseEntity)
    object: BaseEntity | None = Field(default_factory=BaseEntity)
    template: BaseEntity | None = Field(default_factory=BaseEntity)
    project: BaseEntity | None = Field(default_factory=BaseEntity)
    counterparty: PersonResponse = Field(default_factory=PersonResponse)
    dateTime: TimePoint | None = Field(default_factory=TimePoint)
    startDateTime: TimePoint | None = Field(default_factory=TimePoint)
    endDateTime: TimePoint | None = Field(default_factory=TimePoint)
    hasStartDate: bool | None = None
    hasEndDate: bool | None = None
    hasStartTime: bool | None = None
    hasEndTime: bool | None = None
    delayedTillDate: TimePoint | None = Field(default_factory=TimePoint)
    dateOfLastUpdate: TimePoint | None = Field(default_factory=TimePoint)
    duration: int | None = None
    durationUnit: DurationUnit | None = None
    durationType: DurationType | None = None
    overdue: bool | None = None
    closeToDeadLine: bool | None = None
    notAcceptedInTime: bool | None = None
    inFavorites: bool | None = None
    isSummary: bool | None = None
    isSequential: bool | None = None
    assignees: PeopleResponse | None = Field(default_factory=PeopleResponse)
    participants: PeopleResponse | None = Field(default_factory=PeopleResponse)
    auditors: PeopleResponse | None = Field(default_factory=PeopleResponse)
    # recurrence: str
    isDeleted: bool | None = None
    # files: list
    customFieldData: list[CustomFieldValueResponse] | None = Field(default_factory=list)

    def get_custom_field(self, field: CustomFields) -> CustomFieldValueResponse:
        with suppress(StopIteration):
            return next(filter(lambda d: d.field.id == field, self.customFieldData))

    @computed_field
    @cached_property
    def rebill_field(self) -> CustomFieldValueResponse:
        return self.get_custom_field(field=CustomFields.REBILL_ID)

    @computed_field
    @cached_property
    def client_field(self) -> CustomFieldValueResponse:
        return self.get_custom_field(field=CustomFields.CLIENT_ID)


class TaskFilterResponse(BaseModel):
    result: str
    tasks: list[TaskResponse]
