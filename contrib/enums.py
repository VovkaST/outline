import enum
from collections.abc import Iterable


class ChoicesType(enum.EnumMeta):
    """A metaclass for creating an enum choices."""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, list | tuple) and len(value) > 1 and isinstance(value[-1], str):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace("_", " ").title()
            labels.append(label)
            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels, strict=False):
            member._label_ = label
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def choices(cls):
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


class Choices(enum.Enum, metaclass=ChoicesType):
    """Class for creating enumerated choices."""

    @property
    def do_not_call_in_templates(self):
        return True

    @property
    def label(self) -> str:
        return self._label_

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}.{self._name_}"


class TextChoices(str, Choices):
    """Класс для создания текстовых перечислений."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class CaseInsensitiveEnumMixin:
    @classmethod
    def _missing_(cls: Iterable, value: str):
        """Регистронезависимый поиск элементов"""
        value = value.upper()
        for member in cls:
            if member.upper() == value:
                return member
