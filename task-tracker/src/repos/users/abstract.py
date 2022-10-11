from abc import ABC, abstractmethod
from typing import List

from repos.users.models import User, UserRole

class UserRepo(ABC):

    @abstractmethod
    def get_user(self, login: str) -> User:
        pass

    @abstractmethod
    def list_users_by_role(self, role: UserRole) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, login: str, role: UserRole) -> User:
        pass