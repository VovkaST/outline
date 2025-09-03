import logging

import nest_asyncio
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.ext._application import Application

from app_bot.enums import BotCommands
from app_bot.handlers import commands
from app_bot.handlers.messages import user_message_handler
from app_bot.utils.callback_registry import registry

logger = logging.getLogger("bot")


async def add_commands(app: Application):
    commands = []
    for command in BotCommands:
        commands.append(BotCommand(command.value, command.label))
    await app.bot.set_my_commands(commands)


def build_app(token: str):
    return ApplicationBuilder().token(token).build()


async def run_bot(token: str):
    logger.info("🚀 Запуск бота...")
    nest_asyncio.apply()
    app = build_app(token)

    app.add_handler(CommandHandler(BotCommands.START, commands.start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_message_handler))
    app.add_handler(CallbackQueryHandler(registry.handle))

    await add_commands(app)

    app.run_polling()
