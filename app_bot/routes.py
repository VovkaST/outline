import secrets

from aiohttp.web_exceptions import HTTPUnauthorized
from fastapi import APIRouter, Header
from starlette import status
from starlette.requests import Request

from app_bot import dtos
from app_bot.utils.dialogs import handle_new_chat_message, perform_messages_distribution
from root.config import settings
from root.dtos import ErrorResponse, OkResponse
from root.utils.others import get_route_name
from services.planfix.utils import prefetch_form_data

routes = APIRouter(tags=["Bot hooks"], prefix="/api/bot", generate_unique_id_function=get_route_name)


@routes.post(
    "/messages/create/",
    response_model=OkResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def message_create(request: Request):
    """Отправить сообщение пользователю в чат."""

    form_data = await request.form()
    payload = dtos.NewMessageRequest(**prefetch_form_data(form_data.multi_items()))  # type: ignore [call
    if not secrets.compare_digest(str(payload.token), str(settings.REQUEST_TOKEN)):
        raise HTTPUnauthorized()

    await handle_new_chat_message(payload)
    return OkResponse()


@routes.post(
    "/messages/create/custom/",
    response_model=OkResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def message_custom_create(
    request: Request, payload: dtos.CustomMessageRequest, authorization: str = Header(None)
):
    """Отправить свободное сообщение пользователям в чат."""
    if not secrets.compare_digest(str(authorization), str(settings.REQUEST_TOKEN)):
        raise HTTPUnauthorized()

    await perform_messages_distribution(payload)
    return OkResponse()
