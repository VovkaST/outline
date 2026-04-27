from fastapi import APIRouter, Query
from starlette.requests import Request

from app_server import responses
from app_server.enums import PaymentSystems
from root.config import settings
from root.utils.others import get_route_name
from services import wata, yookassa

routes = APIRouter(tags=["Payments v2"], prefix="/v2/payment", generate_unique_id_function=get_route_name)


services_map = {
    PaymentSystems.YOOKASSA: yookassa,
    PaymentSystems.WATA: wata,
}


@routes.get("/init/", response_model=responses.InitPaymentResponseV2)
async def init_payment_v2(
    request: Request,
    task_id: str = Query(description="Идентификатор задачи"),
    amount: int = Query(description="Сумма платежа в копейках (минимум 1000)"),
    customer_email: str = Query(description="Почтовый ящик клиента", default=""),
    description: str = Query(description="Описание платежа", default=""),
    return_url: str = Query(description="URL редиректа успешной оплаты", default=""),
    payment_agent: PaymentSystems = Query(description="Платежная система", default=settings.DEFAULT_PAYMENT_AGENT),
):
    """Инициализировать платеж."""

    service = services_map.get(payment_agent)
    payment = await service.init_payment(
        task_id=task_id,
        amount=amount,
        description=description,
        customer_email=customer_email,
        return_url=return_url,
    )
    return responses.InitPaymentResponseV2.model_validate(payment, from_attributes=True)
