from collections.abc import Callable
from functools import wraps

from telegram import User

from app_bot.utils.dialogs import clear_username, extract_update_and_context
from services import planfix_webchat


def planfix_log_querydata(func: Callable):
    @wraps(func)
    async def decorator(*args, **kwargs):
        update, context = extract_update_and_context(*args, **kwargs)
        if update and context:
            query = update.callback_query
            if query:
                user: User = update.effective_user  # type: ignore [attr-not-none]
                telegram_id = str(user.id)
                username = clear_username(user.username)
                message = f"Нажал кнопку: {query.data}"
                await planfix_webchat.chat.new_message(
                    chat_id=telegram_id, contact_id=telegram_id, contact_name=username, message=message
                )
        return await func(*args, **kwargs)

    return decorator
