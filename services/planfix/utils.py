import re
from collections import defaultdict

from services import planfix_api
from services.planfix.api.rest.responses import GetTaskResponse, TaskFilterResponse, TaskResponse
from services.planfix.exceptions import TaskNotFoundError
from services.planfix.filters import (
    BASE_TELEGRAM_OBJECT_ID,
    LEAD_SOURCE_ID_TELEGRAM,
    BaseTelegramObjectF,
    ComposedGuidUuidF,
    LeadSourceF,
    RequestKeyF,
    TelegramIdF,
)

ATTACHMENTS_REGEXP = re.compile(r"^attachments\[(.+)\]$", re.IGNORECASE)


def prefetch_form_data(form_data: list[tuple[str, str]]) -> dict:
    """
    Функция для преобразования данных формы из Planfix с вложениями в нужный формат.
    Сложность представляет то, что Planfix отправляет вложения в виде полей с именами
    `attachments[url]` и `attachments[name]`, а не в виде списка объектов.
    На выходе функция собирает эти поля в список словарей с ключами `url` и `name` в ключе `attachments`.
    """
    result = {}
    attachments = defaultdict(list)
    for field_name, value in form_data:
        if field_name.startswith("attachments"):
            match = ATTACHMENTS_REGEXP.match(field_name)
            if match:
                attachments[match.group(1)].append(value)
        else:
            result[field_name] = value
    if attachments:
        result["attachments"] = list(
            map(
                lambda z: dict(zip(["url", "name"], z, strict=False)),
                zip(attachments["url"], attachments["name"], strict=False),
            )
        )
    return result


async def get_task(
    task_guid: str | None = None, request_key: str | None = None, telegram_id: int | None = None
) -> TaskResponse:
    assert task_guid or request_key or telegram_id, (
        "Не указан идентификатор задачи, запроса на привязку счета или TelegramId"
    )
    if (task_guid and not task_guid.isdigit()) or not task_guid:
        args = []
        if task_guid:
            args.append(ComposedGuidUuidF(value=task_guid))
        if request_key:
            args.append(RequestKeyF(value=request_key))
        if telegram_id:
            args.append(TelegramIdF(value=telegram_id))
            args.append(BaseTelegramObjectF(value=BASE_TELEGRAM_OBJECT_ID))
            args.append(LeadSourceF(value=LEAD_SOURCE_ID_TELEGRAM))

        response = await planfix_api.task.get_list(*args)
        response = TaskFilterResponse(**response)

        if not response.tasks:
            raise TaskNotFoundError()

        return response.tasks[0]

    response = await planfix_api.task.get(int(task_guid))
    if "status" in response and response["status"] == "404":
        raise TaskNotFoundError()
    task_response = GetTaskResponse(**response)
    return task_response.task
