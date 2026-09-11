"""Подписи параметров ссылок через HMAC.

Параметры ссылки видны клиенту и редактируются в адресной строке; секрет знает только
сервер. Без подписи клиент может изменить URL на своё усмотрение (например, скопировать
параметры чужой ссылки). С подписью — если параметры изменены, подпись не совпадёт, и
сервер отклонит запрос как поддельный.

Подпись вычисляется как HMAC-SHA256 от payload, укороченный до 32 hex-символов.
Проверка идёт через hmac.compare_digest — постоянное время, защита от timing-атак
(когда клиент подбирает подпись посимвольно по времени ответа).
"""

import hashlib
import hmac

SIGNATURE_LENGTH = 32


def sign(payload: str, secret: str) -> str:
    """HMAC-SHA256 от payload, укороченный до SIGNATURE_LENGTH hex-символов."""
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:SIGNATURE_LENGTH]


def is_valid(payload: str, signature: str, secret: str) -> bool:
    """Проверка подписи в постоянном времени.

    Если секрет пуст, возвращает False. Если секрет задан, вычисляет ожидаемую подпись
    и сравнивает через hmac.compare_digest (постоянное время, защита от timing-атак).
    """
    if not secret:
        return False
    expected = sign(payload, secret)
    return hmac.compare_digest(signature, expected)
