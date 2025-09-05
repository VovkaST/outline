import logging
from functools import wraps

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_server.exceptions import PaymentError
from root.exceptions import AppError
from root.utils.requests import response_to_str

logger = logging.getLogger("app_server")


def exception_handler_log(func):
    @wraps(func)
    async def decorator(request: Request, exc: Exception):
        response = await func(request, exc)
        response_str = await response_to_str(response)
        logger.error(f"Request {request.method} {request.url} failed: {response_str}")
        return response

    return decorator


def error_response(error_code: int, message: str, details: str = None, status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "ErrorCode": error_code,
                "Message": message,
                "Details": details,
            }
        ),
    )


@exception_handler_log
async def payment_error_handler(request: Request, exc: PaymentError):
    return error_response(**exc.response.dump_error())


@exception_handler_log
async def app_error_handler(request: Request, exc: AppError):
    return error_response(
        error_code=exc.error_code, message=exc.message, details=str(exc.args[0]) if exc.args else None
    )


@exception_handler_log
async def unknown_error_handler(request: Request, exc: Exception):
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return error_response(error_code=-1, message="Unhandled error", details=str(exc), status_code=status_code)
