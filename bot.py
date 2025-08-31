import asyncio
import logging.config
import os

import click
import telegram

from app_bot.bot import run_bot
from app_bot.config import BotAppConfig

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
@click.pass_context
def run(ctx: click.core.Context):
    bot_settings: BotAppConfig = ctx.obj["bot_settings"]

    print(f"PythonTelegramBot version {telegram.__version__}, using settings '{os.environ.get('SETTINGS_MODULE')}'")
    print("Starting bot...")

    asyncio.run(run_bot(token=bot_settings.TOKEN))


if __name__ == "__main__":
    cli(obj={})
