from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app_server.error_handlers import app_error_handler, payment_error_handler, unknown_error_handler
from app_server.exceptions import AppError, PaymentError
from app_server.routes import api_routes


def init_app(service_name: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=service_name, version=version, description=description)
    app.exception_handler(AppError)(app_error_handler)
    app.exception_handler(PaymentError)(payment_error_handler)
    app.exception_handler(Exception)(unknown_error_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=["*"],
        allow_origins=["*"],
        allow_methods=["*"],
    )

    app.include_router(api_routes)
    app.mount("/", StaticFiles(directory="app_server/assets", html=True, check_dir=True), name="static")
    return app
