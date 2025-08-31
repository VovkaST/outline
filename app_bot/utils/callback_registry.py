__all__ = ["registry"]

from collections.abc import Callable

from telegram import Update
from telegram.ext import ContextTypes


class CallbackRegistry:
    def __init__(self) -> None:
        self.registry: dict[str, Callable] = {}

    def handler(self, *callback_data: str):
        def decorator(func: Callable):
            for _cb in callback_data:
                self.registry[_cb] = func

        return decorator

    def get_handler(self, callback_data: str) -> Callable | None:
        return self.registry.get(callback_data)

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query or not update.callback_query.data:
            return
        handler = self.get_handler(update.callback_query.data)
        if handler:
            await handler(update, context)


registry = CallbackRegistry()
