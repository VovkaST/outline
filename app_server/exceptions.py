from app_server.dtos import PaymentResponse
from root.exceptions import AppError


class PaymentError(Exception):
    def __init__(self, response: PaymentResponse):
        self.response = response


class TokenError(AppError):
    error_code = 1000
    message = "Ошибка токена"


class TaskNotFoundError(AppError):
    error_code = 1001
    message = "Задача не найдена"
