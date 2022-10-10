from functools import lru_cache
from typing import List, Optional

from repos.users.abstract import UserRepo
from repos.users.exceptions import UserNotFoundException
from repos.users.models import User, UserRole

class InMemoryUserRepo(UserRepo):
    
        def __init__(self, initial_users: Optional[List[User]] = None) -> None:
            self.users = []
            self.users_dict = {}
            for user in initial_users or []:
                self.create_user(user.login, user.role)

        def get_user(self, login: str) -> User:
            try:
                idx = self.users_dict[login]
                return self.users[idx]
            except KeyError:
                raise UserNotFoundException(f"User {login} not found")

        def list_users_by_role(self, role: UserRole) -> List[User]:
            return [user for user in self.users if user.role == role]

        def create_user(self, login: str, role: UserRole) -> User:
            user = User(
                login=login,
                role=role,
                )
            idx = len(self.users)
            self.users.append(user)
            self.users_dict[login] = idx

            return user

@lru_cache()
def get_user_repo():
    initial_users = [User(login="avlkozlov", role=UserRole.DEVELOPER), User(login="iivanov", role=UserRole.DEVELOPER)]
    return InMemoryUserRepo(initial_users)