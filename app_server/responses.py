from pydantic import BaseModel, Field


class CheckOrderResponse(BaseModel):
    is_valid: bool


class InitPaymentResponse(BaseModel):
    payment_id: int | None = Field(description="Уникальный идентификатор транзакции в системе Т‑Кассы", default=None)
    url: str | None = Field(description="Ссылка на платежную форму", default=None)
    qr: str | None = Field(description="QR-код на оплату", default=None)


class InitYooKassaPaymentResponse(BaseModel):
    payment_id: str = Field(description="Уникальный идентификатор транзакции в системе YooKassa")
    confirmation_url: str = Field(description="Ссылка на страницу подтверждения платежа")


class PaymentStatusResponse(BaseModel):
    OrderId: str | None = Field(description="Идентификатор заказа в системе мерчанта", default=None)
    Status: str | None = Field(description="Статус транзакции", default=None)
    PaymentId: str | None = Field(description="Идентификатор платежа в системе Т‑Кассы", default=None)


class CreateTaskResponse(BaseModel):
    id: int


class GetTaskKeyResponse(BaseModel):
    key: str | None
