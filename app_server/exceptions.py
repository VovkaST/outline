from app_server.dtos import PaymentResponse
from root.exceptions import AppError


class PaymentError(Exception):
    def __init__(self, response: PaymentResponse):
        self.response = response


class PaymentGatewayError(Exception):
    status_code = 502

    def __init__(self, message: str, details: str | None = None, status_code: int | None = None):
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code
        super().__init__(message)


class TokenError(AppError):
    error_code = 1000
    message = "Ошибка токена"
