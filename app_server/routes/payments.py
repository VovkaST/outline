import asyncio

from aiohttp.web_exceptions import HTTPUnauthorized
from fastapi import APIRouter, Header, Query
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app_server import dtos, responses
from app_server.enums import PaymentStatus
from app_server.exceptions import PaymentError
from app_server.utils import build_fail_url, build_success_url, clean_guid, make_order_uniq_id
from root.config import settings
from root.dtos import RequestStatusResponse
from root.utils.others import get_route_name
from services import payment_api, planfix_api
from services.planfix.api.rest.enums import SubscriptionStatus
from services.planfix.filters import (
    AccountTokenUpdate,
    PaymentSum2Update,
    PaymentSumUpdate,
    RebillIdUpdate,
    RequestKeyUpdate,
    SubscriptionStatusUpdate,
)
from services.planfix.utils import get_task

routes = APIRouter(tags=["Payments"], prefix="/api/payment", generate_unique_id_function=get_route_name)


@routes.get("/init", response_model=responses.InitPaymentResponse)
async def init_payment(
    request: Request,
    task_guid: str = Query(description="Идентификатор заказа"),
    is_recurrent: bool = Query(description="Признак рекуррентности платежа", default=False),
    use_qr: bool = Query(description="Оплата по QR-коду СБП", default=False),
    amount: int = Query(description="Сумма платежа в копейках (минимум 1000)", ge=1000),
    description: str = Query(description="Описание платежа", default=None),
    deadline: int = Query(description="Срок жизни ссылки (дней)", default=0),
):
    """Инициализировать платеж."""
    task = await get_task(task_guid)
    init_response = await payment_api.prepare_payment_init(
        amount=amount,
        description=description or settings.DEFAULT_PAYMENT_DESCRIPTION,
        deadline=deadline or settings.DEFAULT_PAYMENT_DEADLINE,
        order_id=make_order_uniq_id(task_guid),
        customer_key=task.client_field.value,
        customer_phone=task.client_phone,
        is_recurrent=is_recurrent,
        use_qr=use_qr,
        success_url=build_success_url(task_guid),
        fail_url=build_fail_url(task_guid),
    )
    if not init_response.Success:
        raise PaymentError(init_response)

    response = {"payment_id": init_response.PaymentId}

    coroutines = []
    if use_qr:
        coroutines.append(
            planfix_api.task.update(task_id=task.id, customFieldData=[RequestKeyUpdate(init_response.RequestKey)])
        )

    if hasattr(init_response, "PaymentURL"):
        # coroutines.append(planfix_api.task.add_comment(task_id=task.id, description=init_response.PaymentURL))
        response["url"] = init_response.PaymentURL

    if hasattr(init_response, "Data"):
        # coroutines.append(planfix_api.task.add_comment(task_id=task.id, description=init_response.Data))
        response["qr"] = init_response.Data

    await asyncio.gather(*coroutines)
    return response


@routes.post("/status", status_code=status.HTTP_200_OK)
async def payment_status_update(
    request: Request, payload: dtos.NotificationQrRequest | dtos.NotificationPaymentRequest
):
    """Обновить статус платежа через систему HTTP-уведомлений банка."""
    await payment_api.check_token(payload)
    if isinstance(payload, dtos.NotificationQrRequest):
        task = await get_task(request_key=payload.RequestKey)
    else:
        task = await get_task(task_guid=clean_guid(payload.OrderId))

    coroutines = [planfix_api.task.add_comment(task_id=task.id, description=payload.Status)]

    if payload.Status in [PaymentStatus.AUTHORIZED, PaymentStatus.CONFIRMED, PaymentStatus.ACTIVE]:
        fields_to_update = [SubscriptionStatusUpdate(SubscriptionStatus.ACTIVE)]
        if isinstance(payload, dtos.NotificationPaymentRequest):
            fields_to_update.append(RebillIdUpdate(payload.RebillId))
            if payload.Status == PaymentStatus.AUTHORIZED:
                fields_to_update.append(PaymentSumUpdate(payload.Amount))
                fields_to_update.append(PaymentSum2Update(payload.Amount))
        if isinstance(payload, dtos.NotificationQrRequest):
            fields_to_update.append(AccountTokenUpdate(payload.AccountToken))

        coroutines.append(planfix_api.task.update(task_id=task.id, customFieldData=fields_to_update))

    await asyncio.gather(*coroutines)
    return HTMLResponse("OK")


@routes.get(
    "/{payment_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=responses.PaymentStatusResponse,
)
async def get_payment_status(request: Request, payment_id: int):
    """Получить статус платежа по его идентификатору в системе банка."""
    return await payment_api.get_state(payment_id)


@routes.post("/charge", status_code=status.HTTP_200_OK, response_model=RequestStatusResponse)
async def payment_charge(request: Request, payload: dtos.PaymentChargeRequest, authorization: str = Header(None)):
    """Провести автоматический периодический платеж."""
    if authorization != settings.REQUEST_TOKEN:
        raise HTTPUnauthorized()

    task = await get_task(task_guid=clean_guid(payload.task_guid))
    await payment_api.prepare_payment_init(
        amount=payload.amount,
        order_id=payload.task_guid,
        description=payload.description,
        rebill_id=task.rebill_field.value,
        account_token=task.account_token_field.value,
        customer_phone=task.client_phone,
    )
    return {"success": True, "message": "Повторная оплата прошла успешно"}
