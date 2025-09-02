from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app_bot.config import bot_config
from app_bot.const import CONTEXT_HISTORY_KEY
from app_bot.handlers.commands import start
from app_bot.interaction import menus
from app_bot.interaction.buttons import BotButtons
from app_bot.utils.callback_registry import registry
from app_bot.utils.context_history import context_history
from app_server.utils import get_task


@registry.handler(BotButtons.BACKWARD)
async def backward_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    if CONTEXT_HISTORY_KEY in context.user_data:
        history: list[str] = context.user_data[CONTEXT_HISTORY_KEY]
        if len(history) >= 2:
            *__, prev, current = history
            history.pop()
            handler = registry.get_handler(prev)
            if handler:
                modified_update = update.to_dict()
                modified_update["callback_query"]["data"] = prev
                return await handler(Update.de_json(modified_update, update.get_bot()), context)
    await start(update, context)


@registry.handler(BotButtons.CONNECT, BotButtons.KEY_AND_INSTRUCTION)
@context_history(is_beginning=True)
async def connect_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    query: CallbackQuery = update.callback_query
    await query.edit_message_text(**menus.OSMenu.to_message())


@registry.handler(BotButtons.IOS, BotButtons.ANDROID)
@context_history()
async def os_select_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    query: CallbackQuery = update.callback_query
    context.user_data["os"] = query.data
    base_menu = menus.InstallMenu
    buttons = []
    if query.data == BotButtons.IOS:
        buttons.append([InlineKeyboardButton(BotButtons.IOS_DOWNLOAD.label, url=bot_config.APP_URL_IOS)])
    else:
        buttons.append([InlineKeyboardButton(BotButtons.ANDROID_DOWNLOAD.label, url=bot_config.APP_URL_ANDROID)])
    if base_menu.keyboard:
        buttons.extend(base_menu.keyboard.inline_keyboard)
    await query.edit_message_text(text=base_menu.message, reply_markup=InlineKeyboardMarkup(buttons))


@registry.handler(BotButtons.GET_TOKEN)
@context_history()
async def get_token_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return

    user: User = update.effective_user  # type: ignore [attr-not-none]
    telegram_id = user.id
    task = await get_task(telegram_id=telegram_id)
    menu = menus.KeyInfoMenu
    message = menu.format_message(key=task.vpn_key.stringValue)

    await update.callback_query.edit_message_text(text=message, parse_mode=ParseMode.HTML, reply_markup=menu.keyboard)


@registry.handler(BotButtons.MAIN_MENU)
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)
