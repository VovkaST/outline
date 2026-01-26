from abc import abstractmethod
from typing import Any

from services.planfix.api.rest.spec.models import CustomFieldValueRequest


class ITask:
    @abstractmethod
    async def create_with_set_custom_field(
        self, *args: CustomFieldValueRequest, object_id: int, name: str = "", description: str = ""
    ):
        """Функция получения карточки задачи"""

    @abstractmethod
    async def get(self, **kwargs: dict[str, Any]):
        """Функция получения карточки задачи"""

    @abstractmethod
    async def update(self, task_id: int, silent: bool = False, **kwargs: dict[str, Any]):
        """Функция обновления карточки задачи"""

    @abstractmethod
    async def get_list(self, **kwargs: dict[str, Any]):
        """Функция получения списка задач"""

    @abstractmethod
    async def add_comment(self, task_id: int):
        """Функция добавления комментария к задаче"""

    @abstractmethod
    async def get_task_comments(self, *filters: list, task_id: int, **kwargs):
        """Функция фильтрации комментариев к задаче"""
