from collections.abc import Callable
from functools import wraps

from telegram import Update, User

from app_bot.state import get_user_state
from app_bot.utils.dialogs import clear_username, extract_update_and_context
from services import planfix_webchat
from services.planfix.api.rest.responses import TaskResponse
from services.planfix.exceptions import TaskNotFoundError
from services.planfix.utils import get_task


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


async def store_task_to_context(update: Update, task: TaskResponse | None) -> None:
    await get_user_state().set_task(update.effective_user.id, task)  # type: ignore [union-attr]


async def get_task_from_context(update: Update) -> TaskResponse | None:
    return await get_user_state().get_task(update.effective_user.id)  # type: ignore [union-attr]


def planfix_task_context(func: Callable):
    @wraps(func)
    async def decorator(*args, **kwargs):
        update, context = extract_update_and_context(*args, **kwargs)
        if update and context and not await get_task_from_context(update):
            user: User = update.effective_user  # type: ignore [attr-not-none]
            try:
                task = await get_task(telegram_id=user.id)
            except TaskNotFoundError:
                task = None
            await store_task_to_context(update, task)
        return await func(*args, **kwargs)

    return decorator
