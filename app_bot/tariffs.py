"""Список тарифов из JSON-конфига.

БД в проекте нет, поэтому тарифы задаются файлом (`BOT_TARIFFS_CONFIG`, по умолчанию
`app_bot/tariffs.json`). Файл читается лениво один раз при первом обращении и кэшируется
через `@lru_cache` — правка JSON без перезапуска процесса не подхватывается (это ожидаемо).

Модуль общий для бота (клавиатура выбора тарифа) и сервера (`/tg/go/run` — сумма платежа).
"""

import json
from functools import lru_cache

from pydantic import BaseModel

from root.config import settings


class Tariff(BaseModel):
    id: str
    title: str  # готовый текст кнопки
    price: int  # рубли


@lru_cache(maxsize=1)
def get_tariffs() -> tuple[Tariff, ...]:
    """Все тарифы из конфига. Читает файл один раз, дальше отдаёт из кэша."""
    with open(settings.BOT_TARIFFS_CONFIG, encoding="utf-8") as f:
        raw = json.load(f)
    return tuple(Tariff(**item) for item in raw["tariffs"])


def get_tariff(tariff_id: str) -> Tariff | None:
    """Тариф по идентификатору либо `None`, если такого нет."""
    return next((t for t in get_tariffs() if t.id == tariff_id), None)
