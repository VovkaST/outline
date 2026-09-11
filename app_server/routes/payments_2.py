from fastapi import APIRouter, HTTPException, Query
from starlette import status
from starlette.requests import Request

from app_server import responses
from app_server.enums import PaymentSystems
from app_server.utils import DEFAULT_PAYMENT_AGENT, get_payment_service
from root.utils.others import get_route_name

routes = APIRouter(tags=["Payments v2"], prefix="/v2/payment", generate_unique_id_function=get_route_name)


_PAYMENT_AGENT_QUERY = Query(default=DEFAULT_PAYMENT_AGENT, description="Платежная система")


@routes.get("/init/", response_model=responses.InitPaymentResponseV2)
async def init_payment_v2(
    request: Request,
    task_id: str = Query(description="Идентификатор задачи"),
    amount: int = Query(description="Сумма платежа в копейках (минимум 1000)"),
    customer_email: str = Query(description="Почтовый ящик клиента", default=""),
    description: str = Query(description="Описание платежа", default=""),
    return_url: str = Query(description="URL редиректа успешной оплаты", default=""),
    payment_agent: PaymentSystems = _PAYMENT_AGENT_QUERY,
):
    """Инициализировать платеж."""

    service = get_payment_service(payment_agent)

    if not service:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неизвестная платежная система")

    if not task_id.isdigit():
        from services.planfix.utils import get_task

        task = await get_task(task_guid=task_id)
        task_id = str(task.id)

    payment = await service.init_payment(
        task_id=task_id,
        amount=amount,
        description=description,
        customer_email=customer_email,
        return_url=return_url,
    )
    return responses.InitPaymentResponseV2.model_validate(payment, from_attributes=True)
