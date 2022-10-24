from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    DEVELOPER = "developer"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"


@dataclass
class User:
    login: str
    role: UserRole

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            login=data["login"],
            role=UserRole(data["role"]),
        )