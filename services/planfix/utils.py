import re
from collections import defaultdict

from app_server.exceptions import TaskNotFoundError
from services import planfix_api
from services.planfix.api.rest.responses import TaskFilterResponse, TaskResponse
from services.planfix.filters import GuidF, RequestKeyF, TelegramIdF

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
    args = []
    if task_guid:
        args.append(GuidF(value=task_guid))
    if request_key:
        args.append(RequestKeyF(value=request_key))
    if telegram_id:
        args.append(TelegramIdF(value=telegram_id))
    response = await planfix_api.task.get_list(*args)
    response = TaskFilterResponse(**response)

    if not response.tasks:
        raise TaskNotFoundError()

    return response.tasks[0]
