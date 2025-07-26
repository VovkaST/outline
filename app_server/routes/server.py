from fastapi import APIRouter
from starlette.requests import Request

from app_server import responses
from root.utils.others import get_route_name

routes = APIRouter(tags=["Server"], prefix="/api", generate_unique_id_function=get_route_name)


@routes.get("/health", response_model=responses.RequestStatusResponse)
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return {"success": True, "message": "OK"}
