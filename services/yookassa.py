import logging
import uuid

from yookassa import Configuration, Payment

from app_server.dtos import InitYooKassaPaymentDTO
from services import yookassa_config

logger = logging.getLogger("app_server")


class YooKassaService:
    def __init__(self, account_id: str, token: str) -> None:
        self.account_id = account_id
        self.token = token

        Configuration.configure(self.account_id, self.token, logger=logger)

    def init_payment(
        self,
        task_id: str,
        amount: int,
        description: str = "",
        customer_email: str = "",
    ) -> InitYooKassaPaymentDTO:
        _amount = amount / 100
        payment = Payment.create(
            {
                "amount": {
                    "value": _amount,
                    "currency": yookassa_config.DEFAULT_CURRENCY,
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": yookassa_config.USE_SUCCESS_PAYMENT_REDIRECT_URL,
                },
                "capture": True,
                "description": task_id,
                "metadata": {
                    "order_id": task_id,
                },
                "receipt": {
                    "customer": {
                        "email": customer_email or f"{task_id}@example.com",
                    },
                    "items": [
                        {
                            "description": description or task_id,
                            "quantity": 1.000,
                            "amount": {"value": _amount, "currency": "RUB"},
                            "vat_code": 1,
                            "payment_mode": "full_prepayment",
                            "payment_subject": "service",
                        }
                    ],
                },
            },
            idempotency_key=uuid.uuid4(),
        )
        return InitYooKassaPaymentDTO(payment_id=payment.id, confirmation_url=payment.confirmation.confirmation_url)
