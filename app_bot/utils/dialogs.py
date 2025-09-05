import asyncio

import aiohttp
import filetype
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Update,
)
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext._callbackcontext import CallbackContext

from app_bot.config import bot_config
from app_bot.const import NO_USERNAME
from app_bot.dtos import DistributionRequest, MessageAttachment, NewMessageRequest
from app_bot.exceptions import ChatNotFoundError
from root.utils.others import download_file
from services.planfix.api.rest.responses import TaskResponse


def extract_update_and_context(*args, **kwargs) -> tuple[Update | None, CallbackContext | None]:
    update, context = None, None
    for arg in args + tuple(kwargs.values()):
        if isinstance(arg, CallbackContext):
            context = arg
        elif isinstance(arg, Update):
            update = arg
        if update and context:
            break
    return update, context


def clear_username(username: str | None) -> str:
    return f"@{username}" if username else NO_USERNAME


def make_ref_link(bot, task: TaskResponse) -> str:
    return f"{bot.link}?start=REF{task.id}"


AttachmentFile = InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo


def media_to_input_file(file: bytes) -> AttachmentFile:
    if filetype.is_image(file):
        return InputMediaPhoto(file)
    if filetype.is_video(file):
        return InputMediaVideo(file)
    if filetype.is_audio(file):
        return InputMediaAudio(file)
    return InputMediaDocument(file)


async def prepare_media(attachments: list[MessageAttachment]) -> list[AttachmentFile]:
    async with aiohttp.ClientSession() as session:
        coroutines = []
        for attachment in attachments:
            coroutines.append(download_file(session, attachment.url))
        media = await asyncio.gather(*coroutines)
    return [media_to_input_file(f) for f in media if f]


async def send_message_to_user(
    app,
    *,
    chat_id: int,
    text: str,
    reply_markup=None,
    parse_mode=ParseMode.HTML,
    silent_no_chat: bool = False,
    attachments: list[MessageAttachment] | None = None,
):
    try:
        if attachments and (media := await prepare_media(attachments)):
            return await app.bot.send_media_group(chat_id=chat_id, media=media, caption=text, parse_mode=parse_mode)
        await app.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)
    except BadRequest as error:
        if "Chat not found" in error.message:
            if silent_no_chat:
                return
            raise ChatNotFoundError from error
        raise error


async def perform_messages_distribution(payload: DistributionRequest):
    """Отправить сообщения пользователям в чат."""
    from app_bot.bot import build_app

    inlines = []
    for button_data in payload.inline_keyboard:
        button = InlineKeyboardButton(**button_data.model_dump())
        inlines.append([button])

    message = {
        "text": payload.message,
        "reply_markup": InlineKeyboardMarkup(inlines) if inlines else None,
        "parse_mode": ParseMode.HTML,
    }

    app = build_app(bot_config.TOKEN)
    coroutines = []
    for chat_id in payload.telegram_ids:
        coroutines.append(send_message_to_user(app=app, chat_id=chat_id, **message, silent_no_chat=True))

    await asyncio.gather(*coroutines)


async def handle_new_chat_message(payload: NewMessageRequest):
    from app_bot.bot import build_app

    app = build_app(bot_config.TOKEN)
    await send_message_to_user(
        app=app, chat_id=int(payload.chatId), text=payload.message, attachments=payload.attachments
    )
