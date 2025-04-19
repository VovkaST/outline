from abc import abstractmethod


class IContact:
    @abstractmethod
    async def add(self, **kwargs):
        """Функция добавления контакта"""

    @abstractmethod
    async def update(self, **kwargs):
        """Функция обновления информации о клиенте"""

    @abstractmethod
    async def update_custom_data(self, **kwargs):
        """Функция обновления пользовательских полей контакта"""

    @abstractmethod
    async def get(self, **kwargs):
        """Функция получения информации о клиенте"""

    @abstractmethod
    async def get_list(self, **kwargs):
        """Функция получения списка контактов"""

    @abstractmethod
    async def manage_planfix_access(self, **kwargs):
        """Функция позволяет разрешить или запретить доступ для контакта"""

    @abstractmethod
    async def update_user_info(self, **kwargs):
        """Функция обновления информации относящейся к залогиниванию пользователя в системе"""

    @abstractmethod
    async def update_contractors(self, **kwargs):
        """Функция изменение информации о принадлежности контакта к компании"""

    @abstractmethod
    async def get_phone_types(self, **kwargs):
        """Функция позволяет получить список доступных типов телефонных номеров"""

    @abstractmethod
    async def get_group_list(self, **kwargs):
        """Запрос на получение списка групп контактов"""

    @abstractmethod
    async def delete(self, **kwargs):
        """Функция удаления контакта"""
