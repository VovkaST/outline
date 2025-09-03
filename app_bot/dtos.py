from pydantic import BaseModel, Field


class TelegramButton(BaseModel):
    text: str
    callback_data: str | None = Field(
        description="Данные, которые будут отправлены в колбэке боту при нажатии кнопки", default=None
    )
    url: str | None = Field(description="URL, который будет открыт при нажатии кнопки", default=None)


class DistributionRequest(BaseModel):
    telegram_ids: list[int]
    message: str
    inline_keyboard: list[TelegramButton] = Field(default_factory=list)
