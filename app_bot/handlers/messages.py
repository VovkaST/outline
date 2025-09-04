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


async def user_message_with_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = update.message.from_user  # type: ignore [attr-not-none]
    telegram_id = str(user.id)
    username = clear_username(user.username)

    photo_file = await update.message.photo[-1].get_file()
    attachment_name = photo_file.file_path.split("/")[-1]

    await planfix_webchat.chat.new_message(
        chat_id=telegram_id,
        contact_id=telegram_id,
        contact_name=username,
        message="",
        attachment_name=attachment_name,
        attachment_url=photo_file.file_path,
    )
