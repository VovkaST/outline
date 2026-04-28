import pathlib

import aiohttp
from telegram import PhotoSize, Update, User
from telegram.ext import ContextTypes

from app_bot.s3 import s3_client
from app_bot.utils.dialogs import clear_username
from root.utils.others import download_file
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

    async def get_file_path(file: PhotoSize) -> str:
        f = await file.get_file()
        if not s3_client.is_configured:
            return f.file_path
        async with aiohttp.ClientSession() as session:
            file_content = await download_file(session, f.file_path)
        if not file_content:
            return ""
        extension = pathlib.Path(f.file_path).suffix.lstrip(".")
        return await s3_client.upload_file(name=f"{f.file_unique_id}.{extension}", file=file_content)

    file_path = ""
    try:
        if update.message.photo:
            file_path = await get_file_path(update.message.photo[-1])
        elif update.message.effective_attachment:
            file_path = await get_file_path(update.message.effective_attachment)
        message = update.message.caption
    except Exception as e:
        bot = update.get_bot()
        message = f"Пользователь отправил изображение, но возникла ошибка: {e}"
        await bot.send_message(
            chat_id=telegram_id, text="Возникла ошибка отправки изображения. Мы уже разбираемся с этой проблемой."
        )

    await planfix_webchat.chat.new_message(
        chat_id=telegram_id,
        contact_id=telegram_id,
        contact_name=username,
        message=message,
        attachment_name=file_path.split("/")[-1] if file_path else "",
        attachment_url=file_path,
    )
