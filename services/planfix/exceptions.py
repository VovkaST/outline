from root.exceptions import AppError


class TaskNotFoundError(AppError):
    error_code = 1001
    message = "Задача не найдена"
