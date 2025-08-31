from pydantic import BaseModel, ConfigDict, Field
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app_bot.interaction import messages
from app_bot.interaction.buttons import BotButtons


def enum2btn(button_enum: BotButtons) -> InlineKeyboardButton:
    return InlineKeyboardButton(button_enum.label, callback_data=button_enum.name)


class Menu(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: str
    keyboard: InlineKeyboardMarkup | None = Field(default_factory=lambda: InlineKeyboardMarkup([]))

    def format_message(self, **kwargs) -> str | None:
        return self.message.format(**kwargs)

    def to_message(self) -> dict:
        return {
            "text": self.message or "",
            "reply_markup": self.keyboard,
        }


ConnectionMenu = Menu(
    message=messages.WELCOME,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.CONNECT)],
        ]
    ),
)

OSMenu = Menu(
    message=messages.CHOOSE_PLATFORM,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.IOS)],
            [enum2btn(BotButtons.ANDROID)],
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)

InstallMenu = Menu(
    message=messages.CONNECTION_INSTRUCTION,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)
