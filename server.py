import os

import click
import uvicorn

from app_server.app import init_app

os.environ.setdefault("SETTINGS_MODULE", "settings.local")


@click.group()
@click.option("--port", default=8000)
@click.option("--host", default="127.0.0.1")
@click.pass_context
def cli(ctx, port: int, host: str):
    from root.config import settings

    ctx.obj["port"] = port or settings.SERVER_PORT
    ctx.obj["host"] = host
    ctx.obj["settings"] = settings


@cli.command()
@click.pass_context
def run(ctx: click.core.Context):
    host: str = ctx.obj["host"]
    port: int = ctx.obj["port"]
    settings = ctx.obj["settings"]

    app = init_app(service_name=settings.SERVICE_NAME)
    # logging.config.dictConfig(ctx.obj["config"]["logging"])
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    cli(obj={})
