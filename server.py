import os

import click
import uvicorn

from app_server.app import init_app

os.environ.setdefault("SETTINGS_MODULE", "settings.local")


@click.group()
@click.option("--host", default="127.0.0.1", help="Адрес хоста для запуска сервера")
@click.option("--port", default=8000, help="Порт сервера")
@click.pass_context
def cli(ctx, port: int, host: str):
    from app_server.config import server_config
    from root.config import settings

    ctx.obj["port"] = port or settings.SERVER_PORT
    ctx.obj["host"] = host
    ctx.obj["settings"] = settings
    ctx.obj["server_settings"] = server_config


@cli.command(help="Запуск API-сервера")
@click.pass_context
def run(ctx: click.core.Context):
    from app_server.config import ServerAppConfig

    host = ctx.obj["host"]
    port = ctx.obj["port"]
    settings = ctx.obj["settings"]
    server_settings: ServerAppConfig = ctx.obj["server_settings"]

    app = init_app(
        service_name=settings.SERVICE_NAME,
        version=server_settings.VERSION,
        description=server_settings.DESCRIPTION,
    )
    # logging.config.dictConfig(ctx.obj["config"]["logging"])
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    cli(obj={})
