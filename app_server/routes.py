from fastapi import APIRouter
from starlette.requests import Request

from app_server.responses import SuccessResponse

api_routes = APIRouter(tags=["server"], prefix="/api")


@api_routes.get("/health")
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return SuccessResponse("OK")


@api_routes.get("/get-url")
async def get_url(request: Request):
    """Перемещение расписания в статус 'На согласовании'.
    Доступно только руководителям ГД и из статуса 'Черновик'.
    """
    return SuccessResponse("Черновик отправлен на согласование")
