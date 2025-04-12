from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_server.exceptions import AppError, PaymentError


async def payment_error_handler(request: Request, exc: PaymentError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(exc.response.dump_error()),
    )


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                "ErrorCode": exc.error_code,
                "Message": exc.message,
                "Details": str(exc.args[0]),
            }
        ),
    )


async def unknown_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "ErrorCode": -1,
                "Message": "Unhandled error",
                "Details": str(exc.args[0]),
            }
        ),
    )
