import importlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from app_bot.routes import routes as bot_routes
from app_server import routes
from app_server.error_handlers import (
    app_error_handler,
    payment_error_handler,
    payment_gateway_error_handler,
    unknown_error_handler,
)
from app_server.exceptions import PaymentError, PaymentGatewayError
from root.config import settings
from root.exceptions import AppError
from services.http_service import BaseHTTPService

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.DEFAULT_RATE_LIMIT])


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await BaseHTTPService.close_all()


def init_app(service_name: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=service_name, version=version, description=description, lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.exception_handler(AppError)(app_error_handler)
    app.exception_handler(PaymentError)(payment_error_handler)
    app.exception_handler(PaymentGatewayError)(payment_gateway_error_handler)
    app.exception_handler(Exception)(unknown_error_handler)

    add_middlewares(app)

    app.include_router(routes.keys_routes, prefix="/api")
    app.include_router(routes.orders_routes, prefix="/api")
    app.include_router(routes.payments_routes, prefix="/api")
    app.include_router(routes.payments_routes_v2, prefix="/api")
    app.include_router(routes.server_routes, prefix="/api")
    app.include_router(routes.subscription_routes, prefix="/api")
    app.include_router(routes.tasks_routes, prefix="/api")
    app.include_router(bot_routes, prefix="/api")

    @app.get("/openapi.json/", include_in_schema=False)
    async def openapi_trailing_slash():
        return JSONResponse(app.openapi())

    return app
