from __future__ import annotations

from app_server.config import t_bank_config
from app_server.exceptions import TaskNotFoundError
from app_server.services import planfix_api
from app_server.services.planfix.api.rest.responses import TaskFilterResponse, TaskResponse
from app_server.services.planfix.filters import GuidF, RequestKeyF


def make_order_uniq_id(task_guid: str) -> str:
    # suffix = datetime.now().strftime("%y%m%d_%H%M")
    # return f"{task_guid}.{suffix}"
    return task_guid


def build_success_url(task_guid: str) -> str:
    return t_bank_config.USE_SUCCESS_PAYMENT_REDIRECT_URL


def build_fail_url(task_guid: str) -> str:
    return t_bank_config.USE_FAIL_PAYMENT_REDIRECT_URL


async def get_task(task_guid: str = None, request_key: str = None) -> TaskResponse:
    assert task_guid or request_key, "Не указан идентификатор задачи или запроса на привязку счета"
    args = []
    if task_guid:
        args.append(GuidF(value=task_guid))
    if request_key:
        args.append(RequestKeyF(value=request_key))
    response = await planfix_api.task.get_list(*args)
    response = TaskFilterResponse(**response)

    if not response.tasks:
        raise TaskNotFoundError()

    return response.tasks[0]


def clean_guid(guid: str, separator: str = ".") -> str:
    if separator in guid:
        return guid.split(separator, maxsplit=2)[0]
    return guid
