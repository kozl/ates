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
    status: TaskStatus
    assignee: str
    fee: int
    reward: int
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            status=TaskStatus(data["status"]),
            assignee=data["assignee"],
            fee=data["fee"],
            reward=data["reward"]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "assignee": self.assignee,
            "fee": self.fee,
            "reward": self.reward,
        }