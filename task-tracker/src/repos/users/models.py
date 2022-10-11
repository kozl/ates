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