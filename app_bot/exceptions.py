from root.exceptions import AppError


class ChatError(AppError):
    error_code = 1000
    message = "Ошибка чата"


class ChatNotFoundError(AppError):
    error_code = 1001
    message = "Чат не найден"
