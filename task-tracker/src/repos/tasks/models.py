from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus
    assignee: str