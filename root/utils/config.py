import inspect
import os
from typing import Any

from root.utils.others import str2bool, str2int


class BaseAppConfig:
    PREFIX: str = ""

    def __init__(self):
        for attr_name, default_value in inspect.getmembers(self, lambda a: not (inspect.isroutine(a))):
            if attr_name.startswith("_") or attr_name == "PREFIX":
                continue
            setattr(self, attr_name, self._get_from_settings(attr_name, default_value))
        for attr_name, annotation_type in self.__annotations__.items():
            if not hasattr(self, attr_name):
                setattr(self, attr_name, self._get_from_settings(attr_name, annotation_type()))

    def _get_from_settings(self, name: str, default: Any = None):
        from root.config import settings

        return getattr(settings, f"{self.PREFIX.upper()}_{name}", default)


class Environ:
    def get(self, key: str, default: Any = None) -> str:
        return os.environ.get(key, default)

    def as_bool(self, key: str, default: Any = None) -> bool:
        return str2bool(os.environ.get(key, default))

    def as_int(self, key: str, default: Any = None) -> int:
        return str2int(os.environ.get(key, default))
