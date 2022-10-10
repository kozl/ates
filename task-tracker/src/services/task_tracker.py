import random
from typing import List
from functools import lru_cache

from fastapi import Depends

from repos.tasks.abstract import TaskRepo
from repos.users.abstract import UserRepo
from repos.tasks.models import Task, TaskStatus
from repos.users.models import UserRole
from repos.tasks.memory import get_task_repo
from repos.users.memory import get_user_repo
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

    def get_task(self, task_id: str) -> Task:
        try:
            task = self.tasks.get_task(task_id)
        except  RepoTaskNotFoundException:
            raise TaskNotFoundException(f"Task {task_id} not found")
        return task

    def list_tasks(self, assignee: str) -> List[Task]:
        return self.tasks.list_tasks(lambda task: task.assignee == assignee and task.status == TaskStatus.IN_PROGRESS)

    def create_task(self, description: str) -> Task:
        users = self.users.list_users_by_role(UserRole.DEVELOPER)
        if len(users) == 0:
            raise NoUsersFoundException("No developers found")
        assignee = random.choice(users).login
        return self.tasks.create_task(assignee, description)

    def close_task(self, task_id: str, user: str) -> Task:
        try:
            task = self.tasks.get_task(task_id)
        except RepoTaskNotFoundException:
            raise TaskNotFoundException(f"Task {task_id} not found")
        if task.assignee != user:
            raise UserIsNotAssigneeException(f"User {user} is not assigned to task {task_id}")

        task.status = TaskStatus.CLOSED
        return self.tasks.update_task(task_id, task)

    def assign_all_tasks(self):
        tasks = self.tasks.list_tasks(lambda task: task.status == TaskStatus.IN_PROGRESS)
        developers = self.users.list_users_by_role(UserRole.DEVELOPER)
        for task in tasks:
            task.assignee = random.choice(developers).login
            self.tasks.update_task(task.id, task)

@lru_cache()
def get_service(
    task_repo: TaskRepo = Depends(get_task_repo),
    user_repo: UserRepo = Depends(get_user_repo),
    ) -> TaskTrackerService:
    return TaskTrackerService(task_repo, user_repo)
