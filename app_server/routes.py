from fastapi import APIRouter
from starlette.requests import Request

from app_server import dtos
from app_server.exceptions import PaymentError
from app_server.responses import SuccessResponse
from app_server.services.payment import payment_instance

api_routes = APIRouter(tags=["server"], prefix="/api")


@api_routes.get("/health")
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return SuccessResponse("OK")


@api_routes.get("/get-url")
async def get_url(request: Request, task_id: str, customer_key: str, rebill_id: str = None):
    """Получить URL на оплату заказа."""
    response = await payment_instance.prepare_payment_init(
        amount=15000, order_id=task_id, customer_key=customer_key, is_recurrent=True, rebill_id=rebill_id
    )
    if not response.Success:
        raise PaymentError(response)

    return {
        "PaymentURL": response.PaymentURL if hasattr(response, "PaymentURL") else None,
        "PaymentId": response.PaymentId,
    }


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
