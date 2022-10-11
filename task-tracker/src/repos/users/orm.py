import asyncio
from typing import Optional, List
from functools import lru_cache 

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist

from repos.users.models import UserRole, User
from repos.users.abstract import UserRepo
from repos.users.exceptions import UserNotFoundException


class UserORM(models.Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=500, unique=True)
    role = fields.CharEnumField(UserRole)

class ORMUserRepo(UserRepo):

        async def get_user(self, login: str) -> User:
            try:
                user_orm = await UserORM.get(login=login)
            except DoesNotExist:
                raise UserNotFoundException(f"User {login} not found")
            return User(
                login=user_orm.login,
                role=user_orm.role,
            )

        async def list_users_by_role(self, role: UserRole) -> List[User]:
            users_orm = await UserORM.filter(role=role)
            return [User(login=user.login,role=user.role) for user in users_orm]

        async def create_user(self, login: str, role: UserRole) -> User:
            user_orm = UserORM.create(
                login=login,
                role=role,
            )

            return User(
                login=user_orm.login,
                role=user_orm.role,
            )

@lru_cache()
def get_user_repo():
    initial_users = [User(login="avlkozlov", role=UserRole.DEVELOPER), User(login="iivanov", role=UserRole.DEVELOPER)]
    for user in initial_users:
        asyncio.run(UserORM.create(login=user.login, role=user.role))
    return ORMUserRepo()