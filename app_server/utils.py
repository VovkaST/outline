from __future__ import annotations

from app_server.config import t_bank_config
from app_server.enums import PaymentSystems
from root.config import settings

TASK_ID_REDIRECT_PLACEHOLDER = "{task_id}"

DEFAULT_PAYMENT_AGENT = PaymentSystems(settings.DEFAULT_PAYMENT_AGENT)


def get_payment_service(payment_agent: PaymentSystems):
    """Платёжный сервис по идентификатору системы, либо `None`, если он не сконфигурирован.

    Импорт `services` — внутри функции: `services.yookassa`/`services.wata` сами импортируют
    `apply_task_id_to_redirect_url` из этого модуля, и импорт на уровне модуля дал бы цикл.
    """
    from services import wata, yookassa

    services_map = {
        PaymentSystems.YOOKASSA: yookassa,
        PaymentSystems.WATA: wata,
    }
    return services_map.get(payment_agent)


def apply_task_id_to_redirect_url(url: str, task_id: str) -> str:
    """Подставляет task_id в URL, если в шаблоне есть плейсхолдер {task_id}."""
    if TASK_ID_REDIRECT_PLACEHOLDER in url:
        return url.replace(TASK_ID_REDIRECT_PLACEHOLDER, task_id)
    return url


def make_order_uniq_id(task_guid: str) -> str:
    # suffix = datetime.now().strftime("%y%m%d_%H%M")
    # return f"{task_guid}.{suffix}"
    return task_guid


def build_success_url(task_guid: str) -> str:
    return apply_task_id_to_redirect_url(t_bank_config.USE_SUCCESS_PAYMENT_REDIRECT_URL, task_guid)


def build_fail_url(task_guid: str) -> str:
    return t_bank_config.USE_FAIL_PAYMENT_REDIRECT_URL


def clean_guid(guid: str, separator: str = ".") -> str:
    if separator in guid:
        return guid.split(separator, maxsplit=2)[0]
    return guid
