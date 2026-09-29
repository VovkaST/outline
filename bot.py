import logging.config
import os

import click
import telegram

from app_bot.bot import run_bot
from app_bot.config import BotAppConfig
from app_bot.enums import UpdateMode

os.environ.setdefault("SETTINGS_MODULE", "settings.local")


@click.group()
@click.pass_context
def cli(ctx):
    from app_bot.config import bot_config
    from root.config import settings

    logging.config.dictConfig(settings.LOGGING)

    ctx.obj["settings"] = settings
    ctx.obj["bot_settings"] = bot_config


@cli.command(help="Запуск Telegram-бота")
@click.option(
    "--mode",
    type=click.Choice([m.value for m in UpdateMode]),
    default=None,
    help="Способ получения обновлений (по умолчанию — BOT_UPDATE_MODE, иначе polling)",
)
@click.pass_context
def run(ctx: click.core.Context, mode: str | None):
    from app_bot.state import get_user_state

    bot_settings: BotAppConfig = ctx.obj["bot_settings"]
    update_mode = UpdateMode(mode or bot_settings.UPDATE_MODE or UpdateMode.POLLING)

    print(f"PythonTelegramBot version {telegram.__version__}, using settings '{os.environ.get('SETTINGS_MODULE')}'")
    webhook_url = bot_settings.WEBHOOK_URL if update_mode == UpdateMode.WEBHOOK else "not used"
    print(f"Update mode: {update_mode.value}, Webhook URL: {webhook_url}, state storage: {get_user_state().name}")
    print("Starting bot...")

    run_bot(
        token=bot_settings.TOKEN,
        proxy=bot_settings.PROXY_URL or None,
        mode=update_mode,
        webhook_url=bot_settings.WEBHOOK_URL,
        webhook_path=bot_settings.WEBHOOK_PATH,
        webhook_listen=bot_settings.WEBHOOK_LISTEN,
        webhook_port=bot_settings.WEBHOOK_PORT,
        webhook_secret=bot_settings.WEBHOOK_SECRET,
    )


if __name__ == "__main__":
    cli(obj={})
