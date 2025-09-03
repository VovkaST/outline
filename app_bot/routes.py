from aiohttp.web_exceptions import HTTPUnauthorized
from fastapi import APIRouter, Header
from starlette import status
from starlette.requests import Request

from app_bot import dtos
from app_bot.utils.dialogs import perform_messages_distribution
from root.config import settings
from root.dtos import ErrorResponse, OkResponse
from root.utils.others import get_route_name

routes = APIRouter(tags=["Bot hooks"], prefix="/api/bot", generate_unique_id_function=get_route_name)


@routes.post(
    "/distribution/",
    response_model=OkResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def messages_distribution(request: Request, payload: dtos.DistributionRequest, authorization: str = Header(None)):
    """Отправить сообщения пользователям в чат."""
    import secrets

    if not secrets.compare_digest(str(authorization), str(settings.REQUEST_TOKEN)):
        raise HTTPUnauthorized()

    await perform_messages_distribution(payload)
    return OkResponse()
