from collections.abc import Callable
from functools import wraps

from telegram.ext import ContextTypes

from app_bot.const import CONTEXT_HISTORY_KEY
from app_bot.utils.dialogs import extract_update_and_context


def context_history(is_beginning: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            update, context = extract_update_and_context(*args, **kwargs)
            if update and context:
                if CONTEXT_HISTORY_KEY not in context.user_data or is_beginning:
                    clear_or_init_history(context)
                history = context.user_data[CONTEXT_HISTORY_KEY]
                need_to_add = True
                if history:
                    last_loc = history[-1]
                    need_to_add = last_loc != update.callback_query.data
                if need_to_add:
                    context.user_data[CONTEXT_HISTORY_KEY].append(update.callback_query.data)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def clear_or_init_history(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[CONTEXT_HISTORY_KEY] = []
