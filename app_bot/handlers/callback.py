from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from app_bot.config import bot_config
from app_bot.const import CONTEXT_HISTORY_KEY
from app_bot.handlers.commands import start
from app_bot.interaction import menus, messages
from app_bot.interaction.buttons import BotButtons
from app_bot.utils.callback_registry import registry
from app_bot.utils.context_history import context_history
from app_bot.utils.decorators import get_task_from_context, planfix_log_querydata, planfix_task_context
from app_bot.utils.dialogs import make_ref_link
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


@registry.handler(BotButtons.MAIN_MENU)
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


@registry.handler(BotButtons.CONNECT, BotButtons.INSTALL)
@planfix_log_querydata
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
    await query.edit_message_text(
        text=base_menu.message, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML
    )


@registry.handler(BotButtons.GET_TOKEN)
@planfix_log_querydata
@planfix_task_context
@context_history()
async def get_token_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return

    user: User = update.effective_user  # type: ignore [attr-not-none]
    telegram_id = user.id
    task = get_task_from_context(context)
    if not (task or task.vpn_key.stringValue):
        task = await get_task(telegram_id=telegram_id)
    if task.vpn_key.stringValue:
        menu = menus.KeyInfoMenu
        message = menu.format_message(key=task.vpn_key.stringValue)
        await update.callback_query.edit_message_text(
            text=message, parse_mode=ParseMode.HTML, reply_markup=menu.keyboard
        )
    else:
        menu = menus.InstallMenu
        try:
            await update.callback_query.edit_message_text(
                text=messages.KEY_NOT_READY, reply_markup=menu.keyboard, parse_mode=ParseMode.HTML
            )
        except BadRequest as error:
            if "Message is not modified" not in error.message:
                raise


@registry.handler(BotButtons.PAY)
@context_history()
async def pay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    await update.callback_query.edit_message_text(**menus.PayMenu.to_message())


@registry.handler(BotButtons.PAY_1MON, BotButtons.PAY_3MON, BotButtons.PAY_6MON, BotButtons.PAY_12MON)
@planfix_log_querydata
@context_history()
async def tariff_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    button = BotButtons(update.callback_query.data)
    await update.callback_query.edit_message_text(**menus.TariffSelectedMenu.to_message(tariff=button.label))


@registry.handler(BotButtons.REFERAL)
@planfix_log_querydata
@planfix_task_context
@context_history()
async def referal_create_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    task = get_task_from_context(context)
    link = make_ref_link(context.bot, task)
    menu = menus.ReferalMenu
    message = menu.format_message(ref_link=link)
    await update.callback_query.edit_message_text(text=message, parse_mode=ParseMode.HTML, reply_markup=menu.keyboard)


@registry.handler(BotButtons.HELP)
@planfix_log_querydata
@context_history()
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    await update.callback_query.edit_message_text(**menus.HelpMenu.to_message())


@registry.handler(hook=True)
@planfix_log_querydata
async def hook_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Колбэк-обработчик для хуков. Не имеет функционала, кроме логирования нажатых кнопок в Planfix."""
