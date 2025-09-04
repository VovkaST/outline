import secrets

from aiohttp.web_exceptions import HTTPUnauthorized
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from app_bot import dtos
from app_bot.utils.dialogs import handle_new_chat_message
from root.config import settings
from root.dtos import ErrorResponse, OkResponse
from root.utils.others import get_route_name

routes = APIRouter(tags=["Bot hooks"], prefix="/api/bot", generate_unique_id_function=get_route_name)


@routes.post(
    "/messages/create/",
    response_model=OkResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def message_create(request: Request, payload: dtos.NewMessageRequest):
    """Отправить сообщение пользователю в чат."""

    if not secrets.compare_digest(str(payload.token), str(settings.REQUEST_TOKEN)):
        raise HTTPUnauthorized()

    await handle_new_chat_message(payload)
    return OkResponse()
