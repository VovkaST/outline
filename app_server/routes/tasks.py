from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from app_server import responses
from app_server.dtos import StoreTaskKeyRequest
from root.utils.others import get_route_name
from services import planfix_api
from services.planfix.api.rest import responses as planfix_reponses
from services.planfix.api.rest.spec.models import CustomFieldValueRequest
from services.planfix.filters import UserKeyUpdate

routes = APIRouter(tags=["Taks"], prefix="/tasks", generate_unique_id_function=get_route_name)


_task_key_pairs: dict[int, str | None] = {}


@routes.post("/", response_model=responses.CreateTaskResponse)
async def create(request: Request):
    """Создать задачу."""
    result = await planfix_api.task.create_with_set_custom_field(
        CustomFieldValueRequest.model_validate(UserKeyUpdate(42)),
        name="Ключ с сайта",
        description="Ключ с сайта",
        template=666,
    )
    response = planfix_reponses.CreateTaskResponse.model_validate(result)
    _task_key_pairs[response.id] = None
    return responses.CreateTaskResponse(id=response.id)


@routes.post("/{task_id}/key/", status_code=status.HTTP_201_CREATED)
async def store_task_key(request: Request, task_id: str, payload: StoreTaskKeyRequest):
    """Сохранить ключ для задачи."""
    _task_key_pairs.update({int(task_id): payload.key})


@routes.get("/{task_id}/key/", response_model=responses.GetTaskKeyResponse)
async def get_task_key(request: Request, task_id: str):
    """Получить ключ для задачи."""
    return responses.GetTaskKeyResponse(key=_task_key_pairs.pop(int(task_id), None))
