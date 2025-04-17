from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_server.exceptions import AppError, PaymentError


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


async def payment_error_handler(request: Request, exc: PaymentError):
    return error_response(**exc.response.dump_error())


async def app_error_handler(request: Request, exc: AppError):
    return error_response(
        error_code=exc.error_code, message=exc.message, details=str(exc.args[0]) if exc.args else None
    )


async def unknown_error_handler(request: Request, exc: Exception):
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return error_response(error_code=-1, message="Unhandled error", details=str(exc), status_code=status_code)
