from pydantic import BaseModel, Field


class TelegramButton(BaseModel):
    text: str
    callback_data: str | None = Field(
        description="Данные, которые будут отправлены в колбэке боту при нажатии кнопки", default=None
    )
    url: str | None = Field(description="URL, который будет открыт при нажатии кнопки", default=None)


class CustomMessageRequest(BaseModel):
    telegram_ids: list[int]
    message: str
    inline_keyboard: list[TelegramButton] = Field(default_factory=list)


class MessageAttachment(BaseModel):
    name: str
    url: str


class NewMessageRequest(BaseModel):
    cmd: str
    providerId: str
    chatId: str
    token: str
    message: str
    messageId: str
    userName: str
    userLastName: str
    userIco: str
    taskEmail: str
    integration: str
    attachments: list[MessageAttachment] = Field(default_factory=list)
