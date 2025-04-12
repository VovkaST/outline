from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app_server.error_handlers import unknown_error_handler
from app_server.routes import api_routes


def init_app(service_name: str, version: str, description: str) -> FastAPI:
    app = FastAPI(title=service_name, version=version, description=description)
    app.exception_handler(Exception)(unknown_error_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=["*"],
        allow_origins=["*"],
        allow_methods=["*"],
    )

    app.include_router(api_routes)
    return app
