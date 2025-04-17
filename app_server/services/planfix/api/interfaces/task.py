from abc import abstractmethod


class ITask:
    @abstractmethod
    async def get(self, **kwargs):
        """Функция получения карточки задачи"""

    @abstractmethod
    async def update(self, task_id: int, silent: bool = False, **kwargs):
        """Функция обновления карточки задачи"""

    @abstractmethod
    async def get_list(self, **kwargs):
        """Функция получения списка задач"""

    @abstractmethod
    async def add_comment(self, task_id: int):
        """Функция добавления комментария к задаче"""

    @abstractmethod
    async def get_task_comments(self, *filters: list, task_id: int, **kwargs):
        """Функция фильтрации комментариев к задаче"""
