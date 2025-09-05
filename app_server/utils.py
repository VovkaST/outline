from __future__ import annotations

from app_server.config import t_bank_config


def make_order_uniq_id(task_guid: str) -> str:
    # suffix = datetime.now().strftime("%y%m%d_%H%M")
    # return f"{task_guid}.{suffix}"
    return task_guid


def build_success_url(task_guid: str) -> str:
    return t_bank_config.USE_SUCCESS_PAYMENT_REDIRECT_URL


def build_fail_url(task_guid: str) -> str:
    return t_bank_config.USE_FAIL_PAYMENT_REDIRECT_URL


def clean_guid(guid: str, separator: str = ".") -> str:
    if separator in guid:
        return guid.split(separator, maxsplit=2)[0]
    return guid
