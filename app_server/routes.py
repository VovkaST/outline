from aiohttp.web_exceptions import HTTPUnauthorized
from fastapi import APIRouter, Header, Query
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app_server import dtos, responses
from app_server.enums import PaymentStatus
from app_server.exceptions import PaymentError, TaskNotFoundError
from app_server.services import payment_api, planfix_api
from app_server.services.planfix.api.rest.enums import SubscriptionStatus
from app_server.services.planfix.api.rest.responses import TaskFilterResponse
from app_server.services.planfix.filters import GuidF, RebillIdUpdate, SubscriptionStatusUpdate
from app_server.utils import build_fail_url, build_success_url, make_order_uniq_id
from root.config import settings
from root.utils.others import get_route_name

api_routes = APIRouter(tags=["server"], prefix="/api", generate_unique_id_function=get_route_name)


async def get_task(task_guid):
    response = await planfix_api.task.get_list(GuidF(value=task_guid))
    response = TaskFilterResponse(**response)

    if not response.tasks:
        raise TaskNotFoundError()

    return response.tasks[0]


@api_routes.get("/health")
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return responses.SuccessResponse("OK")


@api_routes.get("/order/check", response_model=responses.CheckOrderResponse)
async def check_order(request: Request, task_guid: str = Query(description="Идентификатор заказа")):
    """Проверка наличия заказа в системе."""
    result = await planfix_api.task.get_list(GuidF(value=task_guid))
    return {"is_valid": bool(result.get("tasks", []))}


@api_routes.get("/order/{task_guid}/")
async def get_order(request: Request, task_guid: str):
    return await planfix_api.task.get_list(GuidF(value=task_guid))


@api_routes.get("/payment/init", response_model=responses.InitPaymentResponse)
async def init_payment(
    request: Request,
    task_guid: str = Query(description="Идентификатор заказа"),
    is_recurrent: bool = Query(description="Признак рекуррентности платежа", default=False),
):
    """Инициализировать платеж."""
    task = await get_task(task_guid)
    init_response = await payment_api.prepare_payment_init(
        amount=settings.DEFAULT_PAYMENT_AMOUNT,
        description=settings.DEFAULT_PAYMENT_DESCRIPTION,
        order_id=make_order_uniq_id(task_guid),
        customer_key=task.client_field.value,
        customer_phone=task.client_phone,
        is_recurrent=is_recurrent,
        use_qr=True,
        success_url=build_success_url(task_guid),
        fail_url=build_fail_url(task_guid),
    )
    if not init_response.Success:
        raise PaymentError(init_response)

    response = {"payment_id": init_response.PaymentId}

    if hasattr(init_response, "PaymentURL"):
        await planfix_api.task.add_comment(task_id=task.id, description=init_response.PaymentURL)
        response["url"] = init_response.PaymentURL

    if hasattr(init_response, "Data"):
        await planfix_api.task.add_comment(task_id=task.id, description=init_response.Data)
        response["qr"] = init_response.Data

    return response


@api_routes.post("/payment/status", status_code=status.HTTP_200_OK)
async def payment_status_update(request: Request, payload: dtos.NotificationPaymentRequest):
    """Обновить статус платежа через систему банка."""
    await payment_api.check_token(payload)
    task = await get_task(payload.OrderId)

    await planfix_api.task.add_comment(task_id=task.id, description=payload.Status)

    if payload.Status in [PaymentStatus.AUTHORIZED, PaymentStatus.CONFIRMED]:
        await planfix_api.task.update(
            task_id=task.id,
            customFieldData=[SubscriptionStatusUpdate(SubscriptionStatus.ACTIVE), RebillIdUpdate(payload.RebillId)],
        )
    return HTMLResponse("OK")


@api_routes.get("/payment/{payment_id}/status", status_code=status.HTTP_200_OK)
async def payment_status_update(request: Request, payment_id: str):
    """Получить статус платежа по его идентификатору в системе банка."""
    return await payment_api.get_state(payment_id)


@api_routes.post("/payment/charge", status_code=status.HTTP_200_OK)
async def payment_charge(request: Request, payload: dtos.PaymentChargeRequest, authorization: str = Header(None)):
    """Провести автоматический периодический платеж."""
    if authorization != settings.REQUEST_TOKEN:
        raise HTTPUnauthorized()

    task_guid, payment_data = payload.task_guid.split(".", maxsplit=2)
    task = await get_task(task_guid)
    await payment_api.prepare_payment_init(
        amount=settings.DEFAULT_PAYMENT_AMOUNT,
        order_id=payload.task_guid,
        rebill_id=task.rebill_field.value,
        customer_phone=task.client_phone,
    )
    return HTMLResponse("OK")


@api_routes.patch("/subscription/reject")
async def subscription_reject(request: Request, payload: dtos.SubscriptionRejectRequest):
    """Отменить активную подписку"""
    task = await get_task(payload.task_guid)
    await planfix_api.task.update(
        task_id=task.id, customFieldData=[SubscriptionStatusUpdate(SubscriptionStatus.INACTIVE)]
    )
