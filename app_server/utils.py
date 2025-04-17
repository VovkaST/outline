from __future__ import annotations

from datetime import datetime

from app_server.config import t_bank_config
from root.config import settings


def make_order_uniq_id(task_guid: str) -> str:
    suffix = datetime.now().strftime("%y%m%d_%H%M")
    return f"{task_guid}.{suffix}"


def build_success_url(task_guid: str) -> str:
    if t_bank_config.USE_SUCCESS_PAYMENT_REDIRECT_URL:
        return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=true"


def build_fail_url(task_guid: str) -> str:
    if t_bank_config.USE_FAIL_PAYMENT_REDIRECT_URL:
        return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=false"
