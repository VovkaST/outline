from collections.abc import Callable
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext._callbackcontext import CallbackContext

from app_bot.const import CONTEXT_HISTORY_KEY


def context_history(is_beginning: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            update, context = None, None
            can_add_to_history = False
            for arg in args:
                if isinstance(arg, CallbackContext):
                    context = arg
                elif isinstance(arg, Update):
                    update = arg
                if update and context:
                    can_add_to_history = True
                    break
            if can_add_to_history:
                if CONTEXT_HISTORY_KEY not in context.user_data or is_beginning:
                    clear_or_init_history(context)
                context.user_data[CONTEXT_HISTORY_KEY].append(update.callback_query.data)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def clear_or_init_history(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[CONTEXT_HISTORY_KEY] = []
