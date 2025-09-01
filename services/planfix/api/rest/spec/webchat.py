from services.planfix.api.base import BaseAPIEntity


class Webchat(BaseAPIEntity):
    async def new_message(
        self,
        chat_id: str,
        contact_id: str,
        contact_name: str,
        message: str,
        channel: str = "",
        contact_last_name: str = "",
        contact_email: str = "",
        contact_phone: str = "",
        contact_data: str = "",
        contact_ico: str = "",
        title: str = "",
        user_email: str = "",
    ):
        """
        :param channel str: `channel` дополнительный идентификатор канала на стороне сторонней системы
            (не обязателен, может использоваться при необходимости).
        :param chat_id str: `chatId` уникальный id чата
        :param message str: `message` содержимое сообщения
        :param title str: `title` заголовок сообщения (если есть, используется для формирования названия задачи)
        :param contact_id str: `contactId` уникальный идентификатор контакта
        :param contact_name str: `contactName` имя контакта
        :param contact_last_name str: `contactLastName` фамилия контакта
        :param contact_ico str: `contactIco` фото контакта
        :param contact_email str: `contactEmail` email контакта
        :param contact_phone str: `contactPhone` телефон контакта
        :param contact_data str: `contactData` дополнительные данные контакта
        :param user_email str: `userEmail` email сотрудника-автора исходящего сообщения (при отсутствии автором
            будет сотрудник указанный в настройках интеграции, при отсутствии кого-либо и там - сотрудник
            подключавший интеграцию).
        """
        data = {
            "channel": channel,
            "chatId": chat_id,
            "message": message,
            "title": title,
            "contactId": contact_id,
            "contactName": contact_name,
            "contactLastName": contact_last_name,
            "contactIco": contact_ico,
            "contactEmail": contact_email,
            "contactPhone": contact_phone,
            "contactData": contact_data,
            "userEmail": user_email,
        }
        return await self.api.make_request("newMessage", method="post", data=data)
