import logging

import nest_asyncio
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
)
from telegram.ext._application import Application

from app_bot.enums import BotCommands

logger = logging.getLogger("bot")


async def set_commands(app: Application):
    commands = []
    for command in BotCommands:
        commands.append(BotCommand(command.value, command.label))
    await app.bot.set_my_commands(commands)


async def run_bot(token: str):
    logger.info("🚀 Запуск бота...")
    nest_asyncio.apply()
    app = ApplicationBuilder().token(token).build()

    # telegram_app.add_handler(CommandHandler("start", start))
    # telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_message))
    # telegram_app.add_handler(CallbackQueryHandler(handle_button))
    # telegram_app.add_handler(CommandHandler("help", help_command))

    await set_commands(app)

    app.run_polling()
