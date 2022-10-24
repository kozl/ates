from typing import Optional, List
from functools import lru_cache

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist

from repos.tasks.models import TaskStatus, Task
from repos.tasks.abstract import TaskRepo, TaskFilter
from repos.tasks.exceptions import TaskNotFoundException


class TaskORM(models.Model):
    id = fields.IntField(pk=True)
    status = fields.CharEnumField(TaskStatus)
    assignee = fields.CharField(max_length=50)
    fee = fields.IntField()
    reward = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

class ORMTaskRepo(TaskRepo):
    async def get_task(self, task_id: str) -> Task:
        try:
            task = await TaskORM.get(id=task_id)
            return Task(
                id=task.id,
                status=task.status,
                assignee=task.assignee,
                fee=task.fee,
                reward=task.reward,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        except DoesNotExist:
            raise TaskNotFoundException(f"Task {task_id} not found")

    async def list_tasks(self, task_filter: Optional[TaskFilter] = None) -> List[Task]:
        tasks = await TaskORM.all()
        return [
            Task(
                id=task.id,
                status=task.status,
                assignee=task.assignee,
                fee=task.fee,
                reward=task.reward,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks
            if task_filter is None or task_filter(task)
        ]

    async def create_task(self, task_id: str, assignee: str, fee: int, reward: int) -> Task:
        task = TaskORM(
            id=task_id,
            status=TaskStatus.IN_PROGRESS,
            assignee=assignee,
            fee=fee,
            reward=reward,
        )
        await task.save()
        return Task(
            id=task.id,
            status=task.status,
            assignee=task.assignee,
            fee=task.fee,
            reward=task.reward,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def assign_task(self, task_id: str, assignee: str) -> Task:
        try:
            task = await TaskORM.get(id=task_id)
        except DoesNotExist:
            raise TaskNotFoundException(f"Task {task_id} not found")

        task.assignee = assignee
        await task.save()
        return Task(
            id=task.id,
            status=task.status,
            assignee=task.assignee,
            fee=task.fee,
            reward=task.reward,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def close_task(self, task_id: str) -> Task:
        try:
            task = await TaskORM.get(id=task_id)
        except DoesNotExist:
            raise TaskNotFoundException
        task.status = TaskStatus.CLOSED
        await task.save()
        return Task(
            id=task.id,
            status=task.status,
            assignee=task.assignee,
            fee=task.fee,
            reward=task.reward,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

@lru_cache()
def get_task_repo():
    return ORMTaskRepo()