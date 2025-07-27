import pathlib

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.requests import Request

from app_server import dtos
from keys.storage import keys_storage
from root.utils.others import get_route_name

routes = APIRouter(tags=["Keys"], prefix="/api/keys", generate_unique_id_function=get_route_name)


@routes.put("/")
async def create_or_update_key(request: Request, payload: dtos.PutKeyRequest):
    """Создать или изменить ключ доступа."""

    file_name = keys_storage.make_name(payload.guid)
    keys_storage.save(file_name, key=payload.key)


@routes.get("/{key_id}")
async def get_key_file(request: Request, key_id: str):
    """Получить файл ключа доступа."""
    path = keys_storage.get(key_id)
    file_name = pathlib.Path(path).name
    return FileResponse(path, filename=file_name)
