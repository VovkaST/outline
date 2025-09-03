from pydantic import BaseModel, ConfigDict, Field
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from app_bot.interaction import messages
from app_bot.interaction.buttons import BotButtons


def enum2btn(button_enum: BotButtons) -> InlineKeyboardButton:
    return InlineKeyboardButton(button_enum.label, callback_data=button_enum.name)


class Menu(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: str
    keyboard: InlineKeyboardMarkup | None = Field(default_factory=lambda: InlineKeyboardMarkup([]))

    def format_message(self, **kwargs) -> str:
        return self.message.format(**kwargs)

    def to_message(self, parse_mode: ParseMode = ParseMode.HTML, **format_message_kwargs) -> dict:
        return {
            "text": self.format_message(**format_message_kwargs) if format_message_kwargs else self.message or "",
            "reply_markup": self.keyboard,
            "parse_mode": parse_mode,
        }


WelcomeMenu = Menu(
    message=messages.WELCOME,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.CONNECT)],
        ]
    ),
)

MainMenu = Menu(
    message=messages.MAIN_MENU,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.PAY)],
            [enum2btn(BotButtons.INSTALL)],
            [enum2btn(BotButtons.REFERAL)],
            [enum2btn(BotButtons.HELP)],
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
            [enum2btn(BotButtons.GET_TOKEN)],
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)

KeyInfoMenu = Menu(
    message=messages.KEY_INFO,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.MAIN_MENU)],
        ]
    ),
)

PayMenu = Menu(
    message=messages.CHOOSE_TARIFF,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.PAY_1MON)],
            [enum2btn(BotButtons.PAY_3MON)],
            [enum2btn(BotButtons.PAY_6MON)],
            [enum2btn(BotButtons.PAY_12MON)],
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)

TariffSelectedMenu = Menu(
    message=messages.TARIFF_SELECTED,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.MAIN_MENU)],
        ]
    ),
)

ReferalMenu = Menu(
    message=messages.REFERAL,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)

HelpMenu = Menu(
    message=messages.HELP,
    keyboard=InlineKeyboardMarkup(
        [
            [enum2btn(BotButtons.BACKWARD)],
        ]
    ),
)
