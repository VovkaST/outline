from __future__ import annotations

from app_server.config import t_bank_config
from app_server.exceptions import TaskNotFoundError
from app_server.services import planfix_api
from app_server.services.planfix.api.rest.responses import TaskFilterResponse, TaskResponse
from app_server.services.planfix.filters import GuidF
from root.config import settings


def make_order_uniq_id(task_guid: str) -> str:
    # suffix = datetime.now().strftime("%y%m%d_%H%M")
    # return f"{task_guid}.{suffix}"
    return task_guid


def build_success_url(task_guid: str) -> str:
    if t_bank_config.USE_SUCCESS_PAYMENT_REDIRECT_URL:
        return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=true"


def build_fail_url(task_guid: str) -> str:
    if t_bank_config.USE_FAIL_PAYMENT_REDIRECT_URL:
        return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=false"


async def get_task(task_guid: str) -> TaskResponse:
    response = await planfix_api.task.get_list(GuidF(value=task_guid))
    response = TaskFilterResponse(**response)

    if not response.tasks:
        raise TaskNotFoundError()

    return response.tasks[0]
