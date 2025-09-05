import logging
import re

from aiohttp import ClientResponseError
from telegram import Update, User
from telegram.ext import ContextTypes

from app_bot.enums import BotCommands
from app_bot.interaction import menus, messages
from app_bot.utils.context_history import clear_or_init_history
from app_bot.utils.decorators import get_task_from_context, planfix_task_context, store_task_to_context
from app_bot.utils.dialogs import clear_username
from services import planfix_webchat
from services.planfix.exceptions import TaskNotFoundError
from services.planfix.utils import get_task

logger = logging.getLogger("bot")

COMMAND_REGEXP = re.compile(r"^/(?P<command>\w+)\s?(?P<referal>\w+)?$")


@planfix_task_context
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    match = COMMAND_REGEXP.match(update.effective_message.text or "") if update.effective_message else None
    is_command: bool = match.group("command") == BotCommands.START if match else False
    user: User = update.effective_user  # type: ignore [attr-not-none]
    telegram_id = user.id
    username = clear_username(user.username)
    chat_id = update.effective_chat.id  # type: ignore [attr-defined]
    bot = update.get_bot()
    is_key_generated = False

    try:
        task = get_task_from_context(context) if not is_command else None
        if not task or not task.vpn_key_link.stringValue:
            task = await get_task(telegram_id=telegram_id)
            store_task_to_context(context, task)
        is_key_generated = bool(task.vpn_key_link.stringValue)
    except TaskNotFoundError:
        task = None

    is_first_visit = not task

    clear_or_init_history(context)
    if is_first_visit or not is_key_generated:
        try:
            if is_command and is_first_visit:
                ref_link: str = ""
                if context.args:
                    ref_link = context.args[0]
                message = (
                    f"✅ Пользователь запустил бота через /start{ref_link}\nID: {telegram_id}\nUsername: {username}"
                )
                await planfix_webchat.chat.new_message(
                    chat_id=str(telegram_id), contact_id=str(telegram_id), contact_name=username, message=message
                )
            await bot.send_message(chat_id=chat_id, **menus.WelcomeMenu.to_message())

        except ClientResponseError as error:
            logger.error("📨 Ошибка отправки данных в Planfix (%s): %s", error.code, error.message)
            await bot.send_message(
                chat_id=chat_id, text=messages.PLANFIX_CONNECTION_ERROR, reply_markup=menus.WelcomeMenu.keyboard
            )
    else:
        menu = menus.MainMenu if is_key_generated else menus.WelcomeMenu
        message_kwargs = menu.to_message()
        if "{first_name}" in message_kwargs["text"]:
            message_kwargs["text"] = menu.format_message(first_name=user.first_name)
        query = update.callback_query
        if query:
            await query.edit_message_text(**message_kwargs)
        else:
            await bot.send_message(chat_id=chat_id, **message_kwargs)
