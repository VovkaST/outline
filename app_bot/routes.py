from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from app_bot import dtos
from app_bot.utils.dialogs import preform_messages_distribution
from root.dtos import ErrorResponse, OkResponse
from root.utils.others import get_route_name

routes = APIRouter(tags=["Bot hooks"], prefix="/api/bot", generate_unique_id_function=get_route_name)


@routes.post(
    "/distribution/",
    response_model=OkResponse,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def messages_distribution(request: Request, payload: dtos.DistributionRequest):
    """Отправить сообщения пользователям в чат."""

    await preform_messages_distribution(payload)
    return OkResponse()
