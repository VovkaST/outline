import re
from datetime import datetime, timedelta

import aiohttp
from starlette import status


def str2bool(s: str) -> bool:
    """Гарантированно вернёт булево значение из строки."""
    if s:
        return str(s).lower() not in ["off", "false", "0", "null", "nil", "none"]
    return False


def str2int(s: str) -> int:
    """Гарантированно вернёт число из строки."""
    if s is None:
        return 0
    try:
        return int(s)
    except ValueError:
        nums = re.findall(r"\d+", s)
        return int(nums[0]) if len(nums) else 0


def get_route_name(route) -> str:
    return route.name


def make_deadline_time(since: datetime, *, days: float = 0, minutes: float = 0, hours: float = 0) -> str:
    deadline = (since + timedelta(days=days, minutes=minutes, hours=hours)).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    return f"{deadline[:22]}:{deadline[22:]}"


async def download_file(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as resp:
        if resp.status == status.HTTP_200_OK:
            return await resp.content.read()
