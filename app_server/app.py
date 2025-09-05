import importlib

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles

from app_bot.routes import routes as bot_routes
from app_server import routes
from app_server.error_handlers import app_error_handler, payment_error_handler, unknown_error_handler
from app_server.exceptions import PaymentError
from root.config import settings
from root.exceptions import AppError


def add_middlewares(app: FastAPI):
    middlewares = settings.MIDDLEWARE

    def _add(app: FastAPI, middleware_class=BaseHTTPMiddleware, **kwargs):
        app.add_middleware(middleware_class, **kwargs)

    for middleware in middlewares:
        if isinstance(middleware, list | tuple):
            middleware, middleware_kwargs = middleware
        else:
            middleware_kwargs = {}
        module_name, middleware_class_name = middleware.rsplit(".", 1)
        module = importlib.import_module(module_name)
        middleware_class = getattr(module, middleware_class_name)
        if not middleware_kwargs:
            _add(app, dispatch=middleware_class)
        else:
            app.add_middleware(middleware_class, **middleware_kwargs)


def init_app(service_name: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=service_name, version=version, description=description)
    app.exception_handler(AppError)(app_error_handler)
    app.exception_handler(PaymentError)(payment_error_handler)
    app.exception_handler(Exception)(unknown_error_handler)

    add_middlewares(app)

    app.include_router(routes.keys_routes)
    app.include_router(routes.orders_routes)
    app.include_router(routes.payments_routes)
    app.include_router(routes.server_routes)
    app.include_router(routes.subscription_routes)
    app.include_router(bot_routes)
    app.mount("/", StaticFiles(directory="app_server/assets", html=True, check_dir=True), name="static")
    return app
