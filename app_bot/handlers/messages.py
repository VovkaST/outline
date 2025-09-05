from telegram import Update, User
from telegram.ext import ContextTypes

from app_bot.utils.dialogs import clear_username
from services import planfix_webchat


async def user_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = update.message.from_user  # type: ignore [attr-not-none]
    text = update.message.text  # type: ignore [attr-not-none]

    telegram_id = str(user.id)
    username = clear_username(user.username)
    await planfix_webchat.chat.new_message(
        chat_id=telegram_id, contact_id=telegram_id, contact_name=username, message=text
    )


async def user_message_with_attachment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = update.message.from_user  # type: ignore [attr-not-none]
    telegram_id = str(user.id)
    username = clear_username(user.username)

    async def get_file_path(file) -> str:
        f = await file.get_file()
        return f.file_path

    file_path = ""
    if update.message.photo:
        file_path = await get_file_path(update.message.photo[-1])
    elif update.message.effective_attachment:
        file_path = await get_file_path(update.message.effective_attachment)

    await planfix_webchat.chat.new_message(
        chat_id=telegram_id,
        contact_id=telegram_id,
        contact_name=username,
        message="",
        attachment_name=file_path.split("/")[-1] if file_path else "",
        attachment_url=file_path,
    )
