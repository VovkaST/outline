from enum import Enum


class Role(str, Enum):
    ASSIGNER = "assigner"
    ASSIGNEE = "assignee"
    AUDITOR = "auditor"
    PARTICIPANT = "participant"


class TypeList(str, Enum):
    COMMENTS = "Comments"
    ALL = "All"
    NEW = "New"
    DELETED = "Deleted"


class OrderDirection(str, Enum):
    ASC = "Asc"
    DESC = "Desc"
