from collections.abc import Callable
from functools import wraps

from telegram import Update

from app_bot.state import get_user_state
from app_bot.utils.dialogs import extract_update_and_context


def context_history(is_beginning: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            update, context = extract_update_and_context(*args, **kwargs)
            if update and context and update.effective_user:
                state = get_user_state()
                if is_beginning:
                    await state.reset_history(update.effective_user.id)
                if update.callback_query and update.callback_query.data:
                    await state.push_history(update.effective_user.id, update.callback_query.data)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def clear_or_init_history(update: Update) -> None:
    if update.effective_user:
        await get_user_state().reset_history(update.effective_user.id)
