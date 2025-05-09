from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):
    def render(self, content):
        message = {"success": True, "message": content}
        return super().render(message)


class CheckOrderResponse(BaseModel):
    is_valid: bool


class InitPaymentResponse(BaseModel):
    payment_id: int | None = Field(title="Уникальный идентификатор транзакции в системе Т‑Кассы", default=None)
    url: str | None = Field(title="Ссылка на платежную форму", default=None)
    qr: str | None = Field(title="QR-код на оплату", default=None)
