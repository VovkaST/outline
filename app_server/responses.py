from pydantic import BaseModel
from starlette.responses import JSONResponse


class SuccessResponse(JSONResponse):
    def render(self, content):
        message = {"success": True, "message": content}
        return super().render(message)


class CheckOrderResponse(BaseModel):
    is_valid: bool


class InitPaymentResponse(BaseModel):
    url: str | None = None
    qr: str | None = None
