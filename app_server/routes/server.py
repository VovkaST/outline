from fastapi import APIRouter
from starlette.requests import Request

from root.dtos import RequestStatusResponse
from root.utils.others import get_route_name

routes = APIRouter(tags=["Server"], generate_unique_id_function=get_route_name)


@routes.get("/health/", response_model=RequestStatusResponse)
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return {"success": True, "message": "OK"}
