import logging

from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.ext._application import Application

from app_bot.enums import BotCommands, UpdateMode
from app_bot.handlers import commands
from app_bot.handlers.messages import (
    user_message_handler,
    user_message_with_attachment_handler,
)
from app_bot.state import close_user_state, get_user_state
from app_bot.utils.callback_registry import registry
from services.http_service import BaseHTTPService

logger = logging.getLogger("bot")


async def add_commands(app: Application):
    commands = []
    for command in BotCommands:
        commands.append(BotCommand(command.value, command.label))
    await app.bot.set_my_commands(commands)


async def on_startup(app: Application) -> None:
    logger.info("🗄 Хранилище состояния бота: %s", get_user_state().name)
    await add_commands(app)


async def on_shutdown(_app: Application) -> None:
    await close_user_state()
    await BaseHTTPService.close_all()


def build_app(token: str, proxy: str | None = None):
    builder = (
        ApplicationBuilder()
        .token(token)
        .concurrent_updates(True)
        .read_timeout(30)
        .write_timeout(30)
        .get_updates_read_timeout(42)
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
    )
    if proxy:
        logger.info("🌐 Бот использует прокси: %s", proxy)
        builder = builder.proxy(proxy).get_updates_proxy(proxy)
    return builder.build()


def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler(BotCommands.START, commands.start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_message_handler))
    app.add_handler(
        MessageHandler(
            filters.VIDEO | filters.VIDEO_NOTE | filters.VOICE | filters.PHOTO | filters.Document.ALL,
            user_message_with_attachment_handler,
        )
    )
    app.add_handler(CallbackQueryHandler(registry.handle))


def run_bot(
    token: str,
    proxy: str | None = None,
    mode: UpdateMode = UpdateMode.POLLING,
    webhook_url: str = "",
    webhook_path: str = "",
    webhook_listen: str = "0.0.0.0",
    webhook_port: int = 8443,
    webhook_secret: str = "",
):
    if mode == UpdateMode.WEBHOOK and not webhook_url:
        raise ValueError("Для режима webhook необходимо задать BOT_WEBHOOK_URL")

    logger.info("🚀 Запуск бота (режим: %s)...", mode.value)
    app = build_app(token, proxy=proxy)
    register_handlers(app)

    try:
        if mode == UpdateMode.WEBHOOK:
            url_path = webhook_path.strip("/")
            # Вебхук при остановке не удаляется: при rolling update апдейты принимают оставшиеся реплики
            app.run_webhook(
                listen=webhook_listen,
                port=webhook_port,
                url_path=url_path,
                webhook_url=f"{webhook_url.rstrip('/')}/{url_path}",
                secret_token=webhook_secret or None,
                drop_pending_updates=False,
            )
        else:
            app.run_polling()
    except Exception:
        logger.exception("Bot %s failed", mode.value)
        raise
