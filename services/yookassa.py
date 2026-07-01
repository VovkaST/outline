import asyncio
import logging
import uuid

from requests.exceptions import RequestException
from starlette import status
from yookassa import Configuration, Payment
from yookassa.domain.exceptions import ApiError

from app_server.dtos import InitYooKassaPaymentDTO
from app_server.exceptions import PaymentGatewayError
from app_server.utils import apply_task_id_to_redirect_url
from root.config import settings
from services import yookassa_config

logger = logging.getLogger("app_server")


class YooKassaService:
    def __init__(self, account_id: str, token: str) -> None:
        self.account_id = account_id
        self.token = token
        self.timeout = settings.YOOKASSA_TIMEOUT

        Configuration.configure(self.account_id, self.token, logger=logger, timeout=self.timeout)

    async def init_payment(
        self,
        task_id: str,
        amount: int,
        description: str = "",
        customer_email: str = "",
        return_url: str = "",
    ) -> InitYooKassaPaymentDTO:
        _amount = amount / 100
        confirmation_return_url = (
            return_url
            if return_url
            else apply_task_id_to_redirect_url(yookassa_config.USE_SUCCESS_PAYMENT_REDIRECT_URL, task_id)
        )
        request_payload = {
            "amount": {
                "value": _amount,
                "currency": yookassa_config.DEFAULT_CURRENCY,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": confirmation_return_url,
            },
            "capture": True,
            "description": task_id,
            "metadata": {
                "order_id": task_id,
            },
            "receipt": {
                "customer": {
                    "email": customer_email or f"task+{task_id}@aspectgroup.planfix.ru",
                },
                "items": [
                    {
                        "description": description or task_id,
                        "quantity": 1.000,
                        "amount": {"value": _amount, "currency": yookassa_config.DEFAULT_CURRENCY},
                        "vat_code": 1,
                        "payment_mode": "full_prepayment",
                        "payment_subject": "service",
                    }
                ],
            },
        }
        logger.debug("Try to create YooKassa payment: %s", request_payload)
        idempotency_key = str(uuid.uuid4())
        try:
            payment = await asyncio.wait_for(
                asyncio.to_thread(Payment.create, request_payload, idempotency_key),
                timeout=self.timeout,
            )
        except TimeoutError as exc:
            logger.error("YooKassa payment create timed out after %s seconds", self.timeout)
            raise PaymentGatewayError(
                "Платежный шлюз не ответил вовремя",
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            ) from exc
        except (RequestException, ApiError) as exc:
            logger.exception("YooKassa request failed")
            raise PaymentGatewayError(
                "Ошибка платежного шлюза",
                details=str(exc),
                status_code=status.HTTP_502_BAD_GATEWAY,
            ) from exc
        logger.debug("Yookassa payment created: %s", payment.json())
        return InitYooKassaPaymentDTO(payment_id=payment.id, confirmation_url=payment.confirmation.confirmation_url)
