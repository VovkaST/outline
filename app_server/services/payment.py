import hashlib

from pydantic import BaseModel

from app_server import dtos
from app_server.config import t_bank_config
from app_server.exceptions import TokenError
from app_server.services.base import BaseHTTPService


class Payment(BaseHTTPService):
    urls = {
        "init": "Init",
        "charge": "Charge",
    }
    API_HOST = t_bank_config.REST_API_URL

    def __init__(self, terminal_id: str, terminal_password: str, **kwargs):
        self.terminal_id = terminal_id
        self.terminal_password = terminal_password
        super().__init__(**kwargs)

    async def make_token(self, base_payload: dict) -> str:
        payload = base_payload | {"Password": self.terminal_password}
        use_keys = [key for key, value in payload.items() if isinstance(value, str | int | bool) and key != "Token"]
        pair_values = []
        for key in sorted(use_keys):
            value = payload[key]
            if isinstance(value, bool):
                value = str(value).lower()
            elif isinstance(value, int):
                value = str(value)
            pair_values.append(value)
        pass_str = "".join(pair_values)
        return hashlib.sha256(pass_str.encode("utf-8")).hexdigest()

    async def check_token(self, payload: dict | type[BaseModel]) -> bool:
        if isinstance(payload, BaseModel):
            payload = payload.model_dump(exclude_unset=True)
        if not payload.get("Token"):
            raise TokenError("Токен отсутствует")
        token = await self.make_token(payload)
        if token != payload["Token"]:
            raise TokenError("Неверный токен")
        return True

    async def prepare_payment_init(
        self,
        amount: int,
        order_id: str,
        customer_key: str,
        description: str = "",
        is_recurrent: bool = True,
        rebill_id: str = None,
    ) -> dtos.InitPaymentResponse | dtos.PaymentResponse:
        response = await self.init(
            amount=amount,
            order_id=order_id,
            description=description,
            customer_key=customer_key if not rebill_id else None,
            is_recurrent=is_recurrent and not rebill_id,
        )
        if rebill_id and response.Success:
            return await self.charge(payment_id=response.PaymentId, rebill_id=rebill_id)
        return response

    async def init(
        self,
        amount: int,
        order_id: str,
        description: str = "",
        customer_key: str = None,
        is_recurrent: bool = True,
    ) -> dtos.InitPaymentResponse:
        payload = {
            "TerminalKey": self.terminal_id,
            "Amount": amount,
            "OrderId": order_id,
            "Description": description,
        }
        if is_recurrent and not customer_key:
            raise ValueError("CustomerKey обязателен для рекуррентных платежей")
        if is_recurrent:
            payload["Recurrent"] = "Y"
        if customer_key:
            payload["CustomerKey"] = customer_key
        payload["Token"] = await self.make_token(payload)
        response = await self.make_request(url_name="init", method="post", json=payload)
        return dtos.InitPaymentResponse(**response)

    async def charge(
        self, payment_id: str, rebill_id: str, ip: str = None, send_email: bool = False, info_email: str = None
    ) -> dtos.PaymentResponse:
        payload = {
            "TerminalKey": self.terminal_id,
            "PaymentId": payment_id,
            "RebillId": rebill_id,
        }
        if ip:
            payload["IP"] = ip
        if send_email:
            if not info_email:
                raise ValueError(
                    "Адрес почты клиента обязателен, если необходима отправка уведомления на почту клиента"
                )
            payload["SendEmail"] = send_email
            payload["InfoEmail"] = info_email
        payload["Token"] = await self.make_token(payload)
        response = await self.make_request(url_name="charge", method="post", payload=payload)
        return dtos.PaymentResponse(**response)
