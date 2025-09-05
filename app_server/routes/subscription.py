from fastapi import APIRouter
from starlette.requests import Request

from app_server import dtos
from root.dtos import RequestStatusResponse
from root.utils.others import get_route_name
from services import planfix_api
from services.planfix.api.rest.enums import SubscriptionStatus
from services.planfix.filters import SubscriptionStatusUpdate
from services.planfix.utils import get_task

routes = APIRouter(tags=["Subscription"], prefix="/api/subscription", generate_unique_id_function=get_route_name)


@routes.patch("/reject", response_model=RequestStatusResponse)
async def subscription_reject(request: Request, payload: dtos.SubscriptionRejectRequest):
    """Отменить активную подписку"""
    task = await get_task(payload.task_guid)
    await planfix_api.task.update(
        task_id=task.id, customFieldData=[SubscriptionStatusUpdate(SubscriptionStatus.INACTIVE)]
    )
    return {"success": True, "message": "Подписка успешно отменена"}
