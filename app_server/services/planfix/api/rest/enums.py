from enum import Enum


class Role(str, Enum):
    ASSIGNER = "assigner"
    ASSIGNEE = "assignee"
    AUDITOR = "auditor"
    PARTICIPANT = "participant"


class Priority(str, Enum):
    NOT_URGENT = "NotUrgent"
    URGENT = "Urgent"


class TypeList(str, Enum):
    COMMENTS = "Comments"
    ALL = "All"
    NEW = "New"
    DELETED = "Deleted"


class OrderDirection(str, Enum):
    ASC = "Asc"
    DESC = "Desc"


class DurationUnit(str, Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


class DurationType(str, Enum):
    CALENDAR_DAY = "CalendarDays"
    WORKER_DAYS = "WorkerDays"
