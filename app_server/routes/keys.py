from fastapi import APIRouter

from root.utils.others import get_route_name

routes = APIRouter(tags=["Keys"], prefix="/api/keys", generate_unique_id_function=get_route_name)
