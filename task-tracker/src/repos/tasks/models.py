from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass
class Task:
    id: str
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    status: TaskStatus
    assignee: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            description=data["description"],
            status=TaskStatus(data["status"]),
            assignee=data["assignee"]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "assignee": self.assignee
        }