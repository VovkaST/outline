from pydantic import BaseModel, Field


class CheckOrderResponse(BaseModel):
    is_valid: bool


class InitPaymentResponse(BaseModel):
    payment_id: int | None = Field(title="Уникальный идентификатор транзакции в системе Т‑Кассы", default=None)
    url: str | None = Field(title="Ссылка на платежную форму", default=None)
    qr: str | None = Field(title="QR-код на оплату", default=None)


class PaymentStatusResponse(BaseModel):
    OrderId: str | None = Field(title="Идентификатор заказа в системе мерчанта", default=None)
    Status: str | None = Field(title="Статус транзакции", default=None)
    PaymentId: str | None = Field(title="Идентификатор платежа в системе Т‑Кассы", default=None)


class RequestStatusResponse(BaseModel):
    success: bool = Field(title="Успешность запроса")
    message: str | None = Field(title="Сообщение о результате запроса", default=None)
