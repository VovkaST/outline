from telegram import Update, User
from telegram.ext import ContextTypes

from app_bot.utils.dialogs import clear_username
from services import planfix_webchat


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = update.effective_user  # type: ignore [attr-not-none]
    text = update.message.text  # type: ignore [attr-not-none]

    telegram_id = str(user.id)
    username = clear_username(user.username)
    message = f"Сообщение от пользователя {username} (ID: {user.id}):\n{text}"
    await planfix_webchat.chat.new_message(
        chat_id=telegram_id, contact_id=telegram_id, contact_name=username, message=message
    )
