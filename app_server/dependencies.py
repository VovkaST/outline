import logging
import secrets
from collections.abc import Awaitable, Callable
from urllib.parse import urlsplit

from fastapi import Security
from fastapi.security import APIKeyHeader
from limits import parse
from starlette.requests import Request

from app_server.exceptions import AccessDeniedError, TooManyRequestsError
from app_server.limiter import get_client_ip, limiter
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


def verify_api_client(browser_rate_limit: str | None = None) -> Callable[..., Awaitable[None]]:
    """Зависимость: пропускает серверных клиентов с валидным X-API-Key и браузерные запросы с разрешённых сайтов.

    Проверка Origin/Referer защищает только от вызовов из браузера с чужих сайтов: вне браузера
    заголовки подделываются, поэтому запросы без ключа ограничиваются `browser_rate_limit` по IP клиента.
    Запросы с ключом под лимит не попадают: с одного IP Планфикса идёт весь поток реальных платежей.
    """
    rate_limit = parse(browser_rate_limit) if browser_rate_limit else None

    async def dependency(request: Request, api_key: str | None = Security(api_key_header)) -> None:
        client_ip = get_client_ip(request)
        if api_key:
            if any(secrets.compare_digest(api_key, key) for key in settings.API_KEYS):
                return
            logger.warning("Отклонён запрос с неверным X-API-Key: %s %s", client_ip, request.url.path)
            raise AccessDeniedError("Неверный ключ API")

        origin = get_request_origin(request)
        if origin not in settings.ALLOWED_ORIGINS:
            logger.warning("Отклонён запрос с недопустимого источника %r: %s %s", origin, client_ip, request.url.path)
            raise AccessDeniedError("Недопустимый источник запроса")

        if rate_limit and not limiter.limiter.hit(rate_limit, request.url.path, client_ip):
            logger.warning("Превышен лимит %s: %s %s", rate_limit, client_ip, request.url.path)
            raise TooManyRequestsError(f"Не более {rate_limit}")

    return dependency
