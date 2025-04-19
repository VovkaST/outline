import re


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
