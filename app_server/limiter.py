from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from root.config import settings


def get_client_ip(request: Request) -> str:
    """IP клиента для rate limit.

    За nginx адрес соединения — это шлюз Docker, общий для всех клиентов; реальный IP nginx кладёт
    в X-Real-IP. Порт API опубликован только на 127.0.0.1, поэтому подставить заголовок в обход nginx нельзя.
    """
    return request.headers.get("x-real-ip") or get_remote_address(request)


limiter = Limiter(key_func=get_client_ip, default_limits=[settings.DEFAULT_RATE_LIMIT])
