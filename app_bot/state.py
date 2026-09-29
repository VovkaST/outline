"""
Хранилище состояния пользователей бота: закэшированная задача Planfix и история навигации по меню.

Если задан `REDIS_URL` — состояние хранится в Redis и общее для всех реплик бота,
иначе — в памяти процесса (теряется при перезапуске, не подходит для нескольких реплик).
"""

import logging
from abc import ABC, abstractmethod

from redis.asyncio import Redis

from app_bot.config import bot_config
from root.config import settings
from services.planfix.api.rest.responses import TaskResponse

logger = logging.getLogger("bot")


class BaseUserState(ABC):
    name: str = ""

    @abstractmethod
    async def get_task(self, user_id: int) -> TaskResponse | None: ...

    @abstractmethod
    async def set_task(self, user_id: int, task: TaskResponse | None) -> None: ...

    @abstractmethod
    async def get_history(self, user_id: int) -> list[str]: ...

    @abstractmethod
    async def reset_history(self, user_id: int) -> None: ...

    @abstractmethod
    async def push_history(self, user_id: int, item: str) -> None:
        """Добавить пункт в историю, если он не совпадает с последним."""

    @abstractmethod
    async def pop_history(self, user_id: int) -> str | None: ...

    async def close(self) -> None:
        return None


class MemoryUserState(BaseUserState):
    name = "memory"

    def __init__(self) -> None:
        self._tasks: dict[int, TaskResponse] = {}
        self._history: dict[int, list[str]] = {}

    async def get_task(self, user_id: int) -> TaskResponse | None:
        return self._tasks.get(user_id)

    async def set_task(self, user_id: int, task: TaskResponse | None) -> None:
        if task:
            self._tasks[user_id] = task
        else:
            self._tasks.pop(user_id, None)

    async def get_history(self, user_id: int) -> list[str]:
        return list(self._history.get(user_id, []))

    async def reset_history(self, user_id: int) -> None:
        self._history[user_id] = []

    async def push_history(self, user_id: int, item: str) -> None:
        history = self._history.setdefault(user_id, [])
        if not history or history[-1] != item:
            history.append(item)

    async def pop_history(self, user_id: int) -> str | None:
        history = self._history.get(user_id)
        return history.pop() if history else None


class RedisUserState(BaseUserState):
    name = "redis"

    def __init__(self, url: str, prefix: str, ttl: int) -> None:
        self._redis = Redis.from_url(url, decode_responses=True)
        self._prefix = prefix
        self._ttl = ttl

    def _key(self, user_id: int, name: str) -> str:
        return f"{self._prefix}:user:{user_id}:{name}"

    async def get_task(self, user_id: int) -> TaskResponse | None:
        raw = await self._redis.get(self._key(user_id, "task"))
        if not raw:
            return None
        try:
            return TaskResponse.model_validate_json(raw)
        except ValueError:
            # Формат модели мог измениться между релизами — просто перезапросим задачу
            logger.warning("Не удалось разобрать задачу пользователя %s из Redis", user_id)
            return None

    async def set_task(self, user_id: int, task: TaskResponse | None) -> None:
        key = self._key(user_id, "task")
        if task:
            await self._redis.set(key, task.model_dump_json(), ex=self._ttl)
        else:
            await self._redis.delete(key)

    async def get_history(self, user_id: int) -> list[str]:
        return await self._redis.lrange(self._key(user_id, "history"), 0, -1)

    async def reset_history(self, user_id: int) -> None:
        await self._redis.delete(self._key(user_id, "history"))

    async def push_history(self, user_id: int, item: str) -> None:
        key = self._key(user_id, "history")
        if await self._redis.lindex(key, -1) == item:
            return
        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.rpush(key, item).expire(key, self._ttl).execute()

    async def pop_history(self, user_id: int) -> str | None:
        return await self._redis.rpop(self._key(user_id, "history"))

    async def close(self) -> None:
        await self._redis.aclose()


def build_user_state() -> BaseUserState:
    if settings.REDIS_URL:
        return RedisUserState(settings.REDIS_URL, prefix=bot_config.STATE_KEY_PREFIX, ttl=bot_config.STATE_TTL)
    return MemoryUserState()


_user_state: BaseUserState | None = None


def get_user_state() -> BaseUserState:
    global _user_state
    if _user_state is None:
        _user_state = build_user_state()
    return _user_state


async def close_user_state() -> None:
    global _user_state
    if _user_state is not None:
        await _user_state.close()
        _user_state = None
