__all__ = ["registry"]

from collections.abc import Callable

from telegram import Update
from telegram.ext import ContextTypes

from app_bot.config import bot_config


class CallbackRegistry:
    def __init__(self) -> None:
        self.registry: dict[str, Callable] = {}
        self.hook_handler: Callable | None = None

    def handler(self, *callback_data: str, hook: bool = False):
        def decorator(func: Callable):
            if hook:
                self.hook_handler = func
            else:
                for _cb in callback_data:
                    self.registry[_cb] = func

        return decorator

    def get_handler(self, callback_data: str) -> Callable | None:
        return self.registry.get(callback_data)

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query or not update.callback_query.data:
            return
        request_data, handler = update.callback_query.data, None
        if request_data.startswith(bot_config.HOOK_REQUEST_DATA_PREFIX):
            if self.hook_handler:
                handler = self.hook_handler
        else:
            handler = self.get_handler(request_data)
        if handler:
            await handler(update, context)


registry = CallbackRegistry()
