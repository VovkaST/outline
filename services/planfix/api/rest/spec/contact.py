from services.planfix.api.base import BaseAPIEntity
from services.planfix.api.interfaces.contact import IContact


class Contact(BaseAPIEntity, IContact):
    async def add(self, **kwargs):
        pass

    async def update(self, **kwargs):
        pass

    async def update_custom_data(self, **kwargs):
        pass

    async def get(self, **kwargs):
        pass

    async def get_list(self, **kwargs):
        pass

    async def manage_planfix_access(self, **kwargs):
        pass

    async def update_user_info(self, **kwargs):
        pass

    async def update_contractors(self, **kwargs):
        pass

    async def get_phone_types(self, **kwargs):
        pass

    async def get_group_list(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
