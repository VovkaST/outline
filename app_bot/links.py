"""Сборка и разбор защищённых ссылок-редиректов для бота.

Ссылка содержит параметры (action, telegram_id, tariff_id), подписанные HMAC. Клиент не
может подделать ссылку без знания секрета сервера (`BOT_LINK_SECRET`).

Модуль импортируется и ботом (для `build`), и сервером (для `verify`), поэтому не тянет
ни telegram, ни fastapi — только stdlib, `root.config.settings` и `root.utils.signing`.

Эндпоинты, обрабатывающие такие ссылки, — `app_server/routes/redirect.py`:
- `GET /tg/go` — проверяет подпись и отдаёт HTML-прокладку с автопереходом;
- `GET /tg/go/run` — снова проверяет подпись, создаёт платёж и редиректит на оплату.
"""

import time
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from root.config import settings
from root.utils.signing import is_valid, sign

PATH = "/tg/go"
PATH_RUN = "/tg/go/run"
LINK_TTL_DAYS = 7


def build(action: str, ttl_days: int = LINK_TTL_DAYS, **params: str | int) -> str:
    """Сборка защищённой ссылки.

    Если `BOT_LINK_SECRET` пуст, возвращает пустую строку (вызывающий рисует фолбэк или
    вовсе не показывает кнопку). Иначе возвращает полный URL с параметрами и подписью.

    Формат: `{SITE_URL}/tg/go?a=<action>&<params>&e=<expires_ts>&s=<hmac32>`
    """
    secret = settings.BOT_LINK_SECRET
    if not secret:
        return ""

    expires = datetime.now(timezone.utc) + timedelta(days=ttl_days)
    expires_ts = str(int(expires.timestamp()))

    str_params = {str(k): str(v) for k, v in params.items()}
    payload = _payload(action, str_params, expires_ts)
    sig = sign(payload, secret)

    # Значения экранируем: параметр может сам содержать `?`/`=`/`&` — без quote() они
    # распарсились бы как границы соседних query-параметров.
    params_str = "&".join(f"{k}={quote(v, safe='')}" for k, v in str_params.items())
    query_parts = [f"a={action}"]
    if params_str:
        query_parts.append(params_str)
    query_parts.extend([f"e={expires_ts}", f"s={sig}"])

    return f"{settings.SITE_URL}{PATH}?{'&'.join(query_parts)}"


def verify(query: Mapping[str, str]) -> dict[str, str] | None:
    """Проверка подписи и срока действия ссылки.

    Возвращает dict параметров (включая `a`, но без служебных `s` и `e`) либо `None`, если:
    - секрет не задан;
    - нет обязательных параметров (`a`, `e`, `s`);
    - `e` не число или срок действия истёк;
    - подпись невалидна.
    """
    secret = settings.BOT_LINK_SECRET
    if not secret:
        return None

    try:
        action = query.get("a", "")
        expires_ts_str = query.get("e", "")
        signature = query.get("s", "")

        if not action or not expires_ts_str or not signature:
            return None

        try:
            expires_ts = int(expires_ts_str)
        except ValueError:
            return None

        if expires_ts < int(time.time()):
            return None

        params_for_check = {k: v for k, v in query.items() if k != "s"}
        payload = _payload(action, params_for_check, expires_ts_str)

        if not is_valid(payload, signature, secret):
            return None

        return {k: v for k, v in query.items() if k not in ("s", "e")}

    except Exception:  # noqa: BLE001
        return None


def _payload(action: str, params: Mapping[str, str], expires: str) -> str:
    """Строка payload'а для подписи.

    Параметры сортируются, чтобы порядок в query-string не влиял на подпись. Значения —
    сырые (не URL-квотированные). Формат: `a=<action>&<отсортированные пары>&e=<expires>`.
    """
    pairs = [f"a={action}"]
    for k in sorted(params.keys()):
        if k not in ("a", "e", "s"):
            pairs.append(f"{k}={params[k]}")
    pairs.append(f"e={expires}")
    return "&".join(pairs)
