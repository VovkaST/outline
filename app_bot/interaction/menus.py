from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app_bot.interaction.buttons import BotButtons


def enum2btn(button_enum: BotButtons) -> InlineKeyboardButton:
    return InlineKeyboardButton(button_enum.label, callback_data=button_enum.name)


connect_menu = InlineKeyboardMarkup(
    [
        [enum2btn(BotButtons.CONNECT)],
    ]
)

os_menu = InlineKeyboardMarkup(
    [
        [enum2btn(BotButtons.IOS)],
        [enum2btn(BotButtons.ANDROID)],
    ]
)
