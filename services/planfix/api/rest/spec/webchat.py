from services.planfix.api.base import BaseAPIEntity
from services.planfix.api.interfaces.webchat import IWebchat


class Webchat(BaseAPIEntity, IWebchat):
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
        attachment_name: str = "",
        attachment_url: str = "",
    ) -> dict:
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
        if attachment_name and attachment_url:
            data["attachments[name]"] = attachment_name
            data["attachments[url]"] = attachment_url
        return await self.api.make_request("newMessage", method="post", data=data)
