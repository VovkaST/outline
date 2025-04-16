from contextlib import suppress
from datetime import datetime

from fastapi import APIRouter, Query
from starlette.requests import Request

from app_server import dtos, responses
from app_server.exceptions import PaymentError
from app_server.services import payment_api, planfix_api
from app_server.services.planfix.api.rest.responses import CustomFieldValueResponse, TaskFilterResponse
from app_server.services.planfix.filters import CustomFields, GuidF
from root.config import settings
from root.utils.others import get_route_name

api_routes = APIRouter(tags=["server"], prefix="/api", generate_unique_id_function=get_route_name)


def get_custom_field(field: CustomFields, field_values: list[CustomFieldValueResponse]) -> CustomFieldValueResponse:
    with suppress(StopIteration):
        return next(filter(lambda d: d.field.id == field, field_values))


def get_rebill_field(fields: list[CustomFieldValueResponse]) -> CustomFieldValueResponse:
    return get_custom_field(field=CustomFields.REBILL_ID, field_values=fields)


def make_order_uniq_id(task_guid: str) -> str:
    suffix = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{task_guid}.{suffix}"


def build_success_url(task_guid: str) -> str:
    return f"{settings.SITE_URL_PAYMENT}/?guid={task_guid}&success=true"


@api_routes.get("/health")
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return responses.SuccessResponse("OK")


@api_routes.get("/order/check", response_model=responses.CheckOrderResponse)
async def check_order(request: Request, task_guid: str = Query(description="Идентификатор заказа")):
    """Проверка наличия заказа в системе."""
    result = await planfix_api.task.get_list(GuidF(value=task_guid))
    return {"is_valid": bool(result.get("tasks", []))}


@api_routes.get("/payment/url", response_model=responses.GetPaymentUrlResponse)
async def get_payment_url(request: Request, task_guid: str = Query(description="Идентификатор заказа")):
    """Получить URL на оплату заказа."""
    response = await planfix_api.task.get_list(GuidF(value=task_guid))
    response = TaskFilterResponse(**response)

    task = response.tasks[0]
    rebill_id_field = get_rebill_field(task.customFieldData)
    response = await payment_api.prepare_payment_init(
        amount=settings.DEFAULT_PAYMENT_AMOUNT,
        order_id=make_order_uniq_id(task_guid),
        customer_key=task.counterparty.id,
        is_recurrent=True,
        rebill_id=rebill_id_field.value,
        success_url=build_success_url(task_guid),
    )
    if not response.Success:
        raise PaymentError(response)

    return {"url": response.PaymentURL}


@api_routes.post("/payment/status")
async def payment_status_update(request: Request, payload: dtos.NotificationPaymentRequest):
    """Обновить статус платежа через систему банка."""
    await payment_instance.check_token(payload)

    # planfix_provider.send_payment_status(
    #     status=payload.Status,
    #     payment_id=payload.PaymentId,
    #     rebill_id=payload.RebillId,
    # )
    return "OK"
