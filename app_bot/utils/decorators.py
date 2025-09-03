from collections.abc import Callable
from functools import wraps

from telegram import User

from app_bot.const import CONTEXT_TASK_KEY
from app_bot.utils.dialogs import clear_username, extract_update_and_context
from app_server.exceptions import TaskNotFoundError
from app_server.utils import get_task
from services import planfix_webchat
from services.planfix.api.rest.responses import TaskResponse


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


def store_task_to_context(context, task) -> None:
    context.user_data[CONTEXT_TASK_KEY] = task


def is_task_in_context(context) -> bool:
    return bool(CONTEXT_TASK_KEY in context.user_data and context.user_data[CONTEXT_TASK_KEY])


def get_task_from_context(context) -> TaskResponse:
    return context.user_data[CONTEXT_TASK_KEY]


def planfix_task_context(func: Callable):
    @wraps(func)
    async def decorator(*args, **kwargs):
        update, context = extract_update_and_context(*args, **kwargs)
        if context and not is_task_in_context(context):
            user: User = update.effective_user  # type: ignore [attr-not-none]
            telegram_id = user.id
            try:
                task = await get_task(telegram_id=telegram_id)
            except TaskNotFoundError:
                task = None
            store_task_to_context(context, task)
        return await func(*args, **kwargs)

    return decorator
