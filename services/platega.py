import logging

import aiohttp
from aiohttp import ClientResponse
from starlette import status

from app_server.dtos import InitPlategaPaymentDTO
from app_server.exceptions import PaymentGatewayError
from app_server.utils import apply_task_id_to_redirect_url
from services import platega_config
from services.http_service import BaseHTTPService

logger = logging.getLogger("app_server")


class PlategaService(BaseHTTPService):
    urls = {
        # Без заданного метода: способ оплаты клиент выбирает на странице Platega
        "process": "v2/transaction/process",
        # С заданным методом (paymentMethod)
        "process_with_method": "transaction/process",
    }
    API_HOST = "https://app.platega.io/"

    def __init__(self, merchant_id: str, secret: str, payment_method: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.merchant_id = merchant_id
        self.secret = secret
        self.payment_method = payment_method

    def get_headers(self, url_name: str, method: str) -> dict:
        headers = super().get_headers(url_name, method)
        headers["X-MerchantId"] = self.merchant_id
        headers["X-Secret"] = self.secret
        return headers

    async def handle_response(self, response: ClientResponse):
        if response.status >= 400:
            details = await response.text()
            logger.error("Platega request failed: %s %s", response.status, details)
            raise PaymentGatewayError(
                "Ошибка платежного шлюза",
                details=details,
                status_code=status.HTTP_502_BAD_GATEWAY,
            )
        return await super().handle_response(response)

    async def init_payment(
        self,
        task_id: str,
        amount: int,
        description: str = "",
        return_url: str = "",
        **kwargs,
    ) -> InitPlategaPaymentDTO:
        success_redirect_url = (
            return_url
            if return_url
            else apply_task_id_to_redirect_url(platega_config.USE_SUCCESS_PAYMENT_REDIRECT_URL, task_id)
        )
        payload = {
            "paymentDetails": {
                "amount": amount / 100,
                "currency": platega_config.DEFAULT_CURRENCY,
            },
            "description": description or task_id,
            "return": success_redirect_url,
            "failedUrl": platega_config.USE_FAIL_PAYMENT_REDIRECT_URL,
            "orderId": task_id,
            "payload": task_id,
            "metadata": {
                "userId": task_id,
            },
        }
        url_name = "process"
        if self.payment_method:
            payload["paymentMethod"] = self.payment_method
            url_name = "process_with_method"
        try:
            response = await self.make_request(url_name=url_name, method="post", json=payload)
        except TimeoutError as exc:
            logger.error("Platega payment create timed out")
            raise PaymentGatewayError(
                "Платежный шлюз не ответил вовремя",
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            ) from exc
        except aiohttp.ClientError as exc:
            logger.exception("Platega request failed")
            raise PaymentGatewayError(
                "Ошибка платежного шлюза",
                details=str(exc),
                status_code=status.HTTP_502_BAD_GATEWAY,
            ) from exc
        return InitPlategaPaymentDTO(**response)
