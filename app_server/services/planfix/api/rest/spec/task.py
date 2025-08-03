from app_server.services.planfix.api.base import BaseAPIEntity
from app_server.services.planfix.api.interfaces.task import ITask
from app_server.services.planfix.api.rest.enums import OrderDirection
from app_server.services.planfix.api.rest.filters import F
from app_server.services.planfix.api.rest.spec import models
from app_server.services.planfix.filters import CustomFields

ALL_FIELDS = [
    "priority",
    "status",
    "processId",
    "resultChecking",
    "type",
    "assigner",
    "parent",
    "pbject",
    "template",
    "project",
    "counterparty",
    "dateTime",
    "startDateTime",
    "endDateTime",
    "hasStartDate",
    "hasEndDate",
    "hasStartTime",
    "hasEndTime",
    "delayedTillDate",
    "dateOfLastUpdate",
    "duration",
    "durationUnit",
    "durationType",
    "overdue",
    "closeToDeadLine",
    "notAcceptedInTime",
    "inFavorites",
    "isSummary",
    "isSequential",
    "assignees",
    "participants",
    "auditors",
    "recurrence",
    "isDeleted",
    "files",
    "sourceObjectId",
    "sourceDataVersion",
]


class Task(BaseAPIEntity, ITask):
    default_fields = [
        "id",
        "name",
        "description",
        CustomFields.GUID.value,
        CustomFields.REBILL_ID.value,
        CustomFields.CLIENT_ID.value,
        CustomFields.SUBSCRIPTION_STATUS_ID.value,
        CustomFields.ACCOUNT_TOKEN.value,
        CustomFields.REQUEST_KEY.value,
        CustomFields.PAYMENT_SUM.value,
    ] + ALL_FIELDS

    def build_fields_list(self, fields: list[str]) -> str:
        return ",".join(self.default_fields + (fields or []))

    def extract_default_filters(self, **kwargs) -> dict:
        _kwargs = {}
        if offset := kwargs.pop("offset", None):
            _kwargs["offset"] = offset
        if page_size := kwargs.pop("pageSize", None):
            _kwargs["pageSize"] = page_size
        return _kwargs

    async def get(self, task_id: int, fields: list[str] = None):
        return await self.api.make_request(
            "get_task", method="get", task_id=task_id, params={"fields": self.build_fields_list(fields)}
        )

    async def update(self, task_id: int, silent: bool = False, **kwargs):
        return await self.api.make_request(
            "update_task",
            method="post",
            task_id=task_id,
            params={"silent": str(silent)},
            json=models.TaskUpdateRequest(**kwargs).model_dump(mode="json", exclude_unset=True),
        )

    async def get_list(self, *filters: list[F], **kwargs):
        _kwargs = self.extract_default_filters(**kwargs)
        fields = kwargs.get("fields", [])
        f = models.Filter(filters=filters, **_kwargs).with_fields(*self.default_fields, *fields)
        return await self.api.make_request("task_list", method="post", json=f.model_dump(mode="json"))

    async def add_comment(self, task_id: int, **kwargs):
        payload = models.AddComment(**kwargs)
        return await self.api.make_request(
            "add_comment", method="post", task_id=task_id, json=payload.model_dump(mode="json", exclude_unset=True)
        )

    async def get_task_comments(self, *filters: list[F], task_id: int, fields: list[str] = None, **kwargs):
        _kwargs = self.extract_default_filters(**kwargs)
        fields = kwargs.get("fields", [])
        order_by = kwargs.get("order_by", [])
        result_order = []
        for field_name in order_by:
            direction = OrderDirection.DESC if field_name.startswith("-") else OrderDirection.ASC
            result_order.append(models.ResultOrder(field=field_name, direction=direction))
        f = models.CommentsFilter(filters=filters, resultOrder=result_order, **kwargs).with_fields(
            *self.default_fields, *fields
        )
        return await self.api.make_request(
            "comments_list", method="post", task_id=task_id, json=f.model_dump(mode="json")
        )
