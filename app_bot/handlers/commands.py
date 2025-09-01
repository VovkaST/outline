import logging

from aiohttp import ClientResponseError
from telegram import Update, User
from telegram.ext import ContextTypes

from app_bot.const import NO_USERNAME
from app_bot.interaction import menus, messages
from app_bot.utils.context_history import clear_or_init_history
from app_server.exceptions import TaskNotFoundError
from app_server.utils import get_task
from services import planfix_webchat

logger = logging.getLogger("bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = update.effective_user  # type: ignore [attr-not-none]
    telegram_id = user.id
    username = f"@{user.username}" if user.username else NO_USERNAME
    chat_id = update.effective_chat.id
    bot = update.get_bot()

    ref_link: str = ""
    if context.args:
        ref_link = context.args[0]

    message = f"✅ Пользователь запустил бота через /start{ref_link}\nID: {telegram_id}\nUsername: {username}"

    try:
        task = await get_task(telegram_id=telegram_id)
    except TaskNotFoundError:
        task = None

    if not task:
        try:
            await planfix_webchat.chat.new_message(
                chat_id=str(telegram_id), contact_id=str(telegram_id), contact_name=username, message=message
            )
            clear_or_init_history(context)
            text = menus.ConnectionMenu.format_message(first_name=user.first_name)
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=menus.ConnectionMenu.keyboard)

        except ClientResponseError as error:
            logger.error("📨 Ошибка отправки данных в Planfix (%s): %s", error.code, error.message)
            await bot.send_message(
                chat_id=chat_id, text=messages.PLANFIX_CONNECTION_ERROR, reply_markup=menus.ConnectionMenu.keyboard
            )
    else:
        pass
