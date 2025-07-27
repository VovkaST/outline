from fastapi import APIRouter, Query
from starlette.requests import Request

from app_server import responses
from app_server.services import planfix_api
from app_server.services.planfix.filters import GuidF
from root.utils.others import get_route_name

routes = APIRouter(tags=["Orders"], prefix="/api/order", generate_unique_id_function=get_route_name)


@routes.get("/check", response_model=responses.CheckOrderResponse)
async def check_order(request: Request, task_guid: str = Query(description="Идентификатор заказа")):
    """Проверка наличия заказа в системе."""
    result = await planfix_api.task.get_list(GuidF(value=task_guid))
    return {"is_valid": bool(result.get("tasks", []))}


@routes.get("/{task_guid}/")
async def get_order(request: Request, task_guid: str):
    return await planfix_api.task.get_list(GuidF(value=task_guid))
