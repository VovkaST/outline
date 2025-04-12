from fastapi import APIRouter
from starlette.requests import Request

from app_server.responses import SuccessResponse
from app_server.services.payment import init_payment

api_routes = APIRouter(tags=["server"], prefix="/api")


@api_routes.get("/health")
async def health(request: Request):
    """Проверка работоспособности сервиса."""
    return SuccessResponse("OK")


@api_routes.get("/get-url")
async def get_url(request: Request, task_id: str, customer_key: str):
    payment = init_payment(task_id, customer_key)
    if payment.Success:
        return {"PaymentURL": payment.PaymentURL, "PaymentId": payment.PaymentId}, 200
    return payment.dump_error(), 400
