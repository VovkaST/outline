import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext._callbackcontext import CallbackContext

from app_bot.config import bot_config
from app_bot.const import NO_USERNAME
from app_bot.dtos import DistributionRequest
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


async def send_message_to_user(
    app, *, chat_id: int, text: str, reply_markup=None, parse_mode=ParseMode.HTML, silent_no_chat: bool = False
):
    try:
        await app.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)
    except BadRequest as error:
        if "Chat not found" in error.message and silent_no_chat:
            return
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
