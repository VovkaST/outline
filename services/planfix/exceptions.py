from root.exceptions import AppError


class TaskNotFoundError(AppError):
    error_code = 1001
    message = "Задача не найдена"


class PlanfixApiError(AppError):
    error_code = 1002
    message = "Ошибка запроса к Планфикс"
