import logging
import secrets
from urllib.parse import urlsplit

from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from app_server.exceptions import AccessDeniedError
from app_server.limiter import get_client_ip
from root.config import settings

logger = logging.getLogger("app_server")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False, description="Ключ серверного клиента (Планфикс)")


def get_request_origin(request: Request) -> str:
    """Источник запроса: Origin, а если его нет — scheme://host из Referer.

    На same-origin GET браузер не отправляет Origin, но отправляет Referer.
    """
    origin = request.headers.get("origin")
    if origin:
        return origin.rstrip("/")
    referer = urlsplit(request.headers.get("referer", ""))
    if referer.scheme and referer.netloc:
        return f"{referer.scheme}://{referer.netloc}"
    return ""


async def verify_api_client(request: Request, api_key: str | None = Security(api_key_header)) -> None:
    """Пропускает серверных клиентов с валидным X-API-Key и браузерные запросы с разрешённых сайтов.

    Проверка Origin/Referer защищает только от вызовов из браузера с чужих сайтов: вне браузера
    заголовки подделываются. От прямых вызовов защищает rate limit эндпоинта.
    """
    if api_key:
        if any(secrets.compare_digest(api_key, key) for key in settings.API_KEYS):
            return
        logger.warning("Отклонён запрос с неверным X-API-Key: %s %s", get_client_ip(request), request.url.path)
        raise AccessDeniedError("Неверный ключ API")

    origin = get_request_origin(request)
    if origin in settings.ALLOWED_ORIGINS:
        return
    logger.warning(
        "Отклонён запрос с недопустимого источника %r: %s %s", origin, get_client_ip(request), request.url.path
    )
    raise AccessDeniedError("Недопустимый источник запроса")
