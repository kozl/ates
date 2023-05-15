import random
from typing import List
from functools import lru_cache

from fastapi import Depends

from repos.tasks.abstract import TaskRepo
from repos.users.abstract import UserRepo
from repos.tasks.models import Task, TaskStatus
from repos.users.models import UserRole
from repos.tasks.orm import get_task_repo
from repos.users.orm import get_user_repo
from repos.tasks.exceptions import TaskNotFoundException as RepoTaskNotFoundException
from repos.users.exceptions import UserNotFoundException as RepoUserNotFoundException

class NoUsersFoundException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class UserIsNotAssigneeException(Exception):
    pass

class TaskNotFoundException(Exception):
    pass


class TaskTrackerService:

    def __init__(self, tasks: TaskRepo, users: UserRepo) -> None:
        self.tasks = tasks
        self.users = users

    async def get_task(self, task_id: str) -> Task:
        try:
            task = await self.tasks.get_task(task_id)
        except  RepoTaskNotFoundException:
            raise TaskNotFoundException(f"Task {task_id} not found")
        return task

    async def list_tasks(self, assignee: str) -> List[Task]:
        return await self.tasks.list_tasks(lambda task: task.assignee == assignee and task.status == TaskStatus.IN_PROGRESS)

    async def create_task(self, title: str, description: str) -> Task:
        users = await self.users.list_users_by_role(UserRole.DEVELOPER)
        if len(users) == 0:
            raise NoUsersFoundException("No developers found")
        assignee = random.choice(users).login
        return await self.tasks.create_task(assignee, title, description)

    async def close_task(self, task_id: str, user: str) -> Task:
        try:
            task = await self.tasks.get_task(task_id)
        except RepoTaskNotFoundException:
            raise TaskNotFoundException(f"Task {task_id} not found")
        if task.assignee != user:
            raise UserIsNotAssigneeException(f"User {user} is not assigned to task {task_id}")

        task.status = TaskStatus.CLOSED
        return await self.tasks.update_task(task_id, task)

    async def assign_all_tasks(self):
        tasks = await self.tasks.list_tasks(lambda task: task.status == TaskStatus.IN_PROGRESS)
        developers = await self.users.list_users_by_role(UserRole.DEVELOPER)
        for task in tasks:
            task.assignee = random.choice(developers).login
            await self.tasks.update_task(task.id, task)

@lru_cache()
def get_service(
    task_repo: TaskRepo = Depends(get_task_repo),
    user_repo: UserRepo = Depends(get_user_repo),
    ) -> TaskTrackerService:
    return TaskTrackerService(task_repo, user_repo)
