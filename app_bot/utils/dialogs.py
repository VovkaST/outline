from telegram import Update
from telegram.ext._callbackcontext import CallbackContext

from app_bot.const import NO_USERNAME


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
