import hashlib
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app_server import dtos
from app_server.config import t_bank_config
from app_server.exceptions import PaymentError, TokenError
from root.utils.others import make_deadline_time
from services.http_service import BaseHTTPService


class Payment(BaseHTTPService):
    urls = {
        "init": "Init",
        "get_qr": "GetQr",
        "get_state": "GetState",
        "charge": "Charge",
        "charge_qr": "ChargeQr",
    }
    API_HOST = t_bank_config.REST_API_URL

    def __init__(self, terminal_id: str, terminal_password: str, taxation: str, **kwargs):
        self.terminal_id = terminal_id
        self.terminal_password = terminal_password
        self.taxation = taxation
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
        deadline: int = 0,
        customer_key: str = None,
        description: str = "",
        customer_phone: str = "",
        customer_email: str = "",
        is_recurrent: bool = True,
        use_qr: bool = False,
        rebill_id: str = None,
        account_token: str = None,
        success_url: str = None,
        fail_url: str = None,
    ) -> dtos.InitPaymentResponse | dtos.PaymentResponse | dtos.GetQrResponse:
        response = await self.init(
            amount=amount,
            order_id=order_id,
            description=description,
            customer_key=customer_key if not rebill_id and not account_token else None,
            customer_phone=customer_phone,
            customer_email=customer_email,
            is_recurrent=(is_recurrent and not rebill_id) or account_token,
            use_qr=use_qr or bool(account_token),
            deadline=deadline,
            success_url=success_url,
            fail_url=fail_url,
        )
        if not response.Success:
            raise PaymentError(response)

        if rebill_id or account_token:
            if rebill_id:
                charge_response = await self.charge(payment_id=response.PaymentId, rebill_id=rebill_id)
            else:
                charge_response = await self.charge_qr(payment_id=response.PaymentId, account_token=account_token)

            if not charge_response.Success:
                raise PaymentError(charge_response)
            return charge_response

        if use_qr:
            qr_response = await self.get_qr(payment_id=response.PaymentId)
            payload_response = await self.get_qr(payment_id=response.PaymentId, type="PAYLOAD")
            qr_response.PaymentURL = payload_response.Data
            return qr_response

        return response

    async def init(
        self,
        amount: int,
        order_id: str,
        deadline: int = 0,
        description: str = "",
        customer_key: str = None,
        customer_phone: str = None,
        customer_email: str = None,
        is_recurrent: bool = True,
        use_qr: bool = False,
        success_url: str = None,
        fail_url: str = None,
    ) -> dtos.InitPaymentResponse:
        if not customer_phone and not customer_email:
            raise ValueError("Номер телефона или почта клиента обязательны для формирования чека")

        payload = {
            "TerminalKey": self.terminal_id,
            "Amount": amount,
            "OrderId": order_id,
            "Description": description,
            "Receipt": {
                "Taxation": self.taxation,
                "Email": customer_email,
                "Phone": customer_phone,
                "Items": [
                    {
                        "Name": "Подписка",
                        "Price": amount,
                        "Quantity": 1,
                        "Amount": amount,
                        "Tax": "none",
                        "PaymentObject": "service",
                    }
                ],
            },
        }
        if deadline:
            payload["RedirectDueDate"] = make_deadline_time(datetime.now(), days=deadline)
        if use_qr:
            payload.update({"DATA": {"QR": True}})
        # if is_recurrent and not customer_key:
        #     raise ValueError("CustomerKey обязателен для рекуррентных платежей")
        if is_recurrent:
            payload["Recurrent"] = "Y"
        if customer_key:
            payload["CustomerKey"] = customer_key
        if success_url:
            payload["SuccessURL"] = success_url
        if fail_url:
            payload["FailURL"] = fail_url
        payload["Token"] = await self.make_token(payload)
        response = await self.make_request(url_name="init", method="post", json=payload)
        return dtos.InitPaymentResponse(**response)

    async def get_qr(self, payment_id: str, type: Literal["IMAGE", "PAYLOAD"] = "IMAGE") -> dtos.GetQrResponse:
        """Метод регистрирует QR и возвращает информацию о нем. Вызывается после метода Init."""
        payload = {"TerminalKey": self.terminal_id, "PaymentId": payment_id, "DataType": type}
        payload["Token"] = await self.make_token(payload)
        response = await self.make_request(url_name="get_qr", method="post", json=payload)
        return dtos.GetQrResponse(**response)

    async def get_state(self, payment_id: str, ip: str = None) -> dtos.PaymentStateResponse:
        """Метод возвращает статус платежа."""
        payload = {"TerminalKey": self.terminal_id, "PaymentId": payment_id}
        if ip:
            payload["IP"] = ip
        payload["Token"] = await self.make_token(payload)
        response = await self.make_request(url_name="get_state", method="post", json=payload)
        return dtos.PaymentStateResponse(**response)

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
        response = await self.make_request(url_name="charge", method="post", json=payload)
        return dtos.PaymentResponse(**response)

    async def charge_qr(
        self, payment_id: str, account_token: str, ip: str = None, send_email: bool = False, info_email: str = None
    ) -> dtos.PaymentQRResponse:
        payload = {
            "TerminalKey": self.terminal_id,
            "PaymentId": payment_id,
            "AccountToken": account_token,
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
        response = await self.make_request(url_name="charge_qr", method="post", json=payload)
        return dtos.PaymentQRResponse(**response)
