from fastapi import APIRouter, Query
from starlette.requests import Request

from app_server import responses
from root.utils.others import get_route_name
from services import yookassa

routes = APIRouter(tags=["Payments v2"], prefix="/v2/payment", generate_unique_id_function=get_route_name)


@routes.get("/init/", response_model=responses.InitYooKassaPaymentResponse)
async def init_yookassa_payment(
    request: Request,
    task_id: str = Query(description="Идентификатор задачи"),
    amount: int = Query(description="Сумма платежа в копейках (минимум 1000)"),
    customer_email: str = Query(description="Почтовый ящик клиента", default=""),
    description: str = Query(description="Описание платежа", default=""),
    return_url: str = Query(description="URL редиректа успешной оплаты", default=""),
):
    """Инициализировать платеж в YooKassa."""
    payment = yookassa.init_payment(
        task_id=task_id, amount=amount, description=description, customer_email=customer_email, return_url=return_url
    )
    return responses.InitYooKassaPaymentResponse.model_validate(payment, from_attributes=True)
