from services.planfix.api.base import BaseAPIEntity
from services.planfix.api.interfaces.contact import IContact


class Contact(BaseAPIEntity, IContact):
    TEMPLATE_FOLDER = "contact/"

    async def add(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.add
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "add.xml", method="post", **kwargs)

    async def update(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.update
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "update.xml", method="post", **kwargs)

    async def update_custom_data(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateCustomData
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "updateCustomData.xml", method="post", **kwargs)

    async def get(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.get
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "get.xml", method="post", **kwargs)

    async def get_list(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getList
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "getList.xml", method="post", **kwargs)

    async def manage_planfix_access(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.managePlanfixAccess
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "managePlanfixAccess.xml", method="post", **kwargs)

    async def update_user_info(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateUserInfo
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "updateUserInfo.xml", method="post", **kwargs)

    async def update_contractors(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateContractors
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "updateContractors.xml", method="post", **kwargs)

    async def get_phone_types(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getPhoneTypes
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "getPhoneTypes.xml", method="post", **kwargs)

    async def get_group_list(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getGroupList
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "getGroupList.xml", method="post", **kwargs)

    async def delete(self, **kwargs):
        """
        https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.delete
        """
        return await self.api.make_request(self.TEMPLATE_FOLDER + "delete.xml", method="post", **kwargs)
