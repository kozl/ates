from typing import Optional, List
from functools import lru_cache

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist

from repos.tasks.models import TaskStatus, Task
from repos.tasks.abstract import TaskRepo, TaskFilter
from repos.tasks.exceptions import TaskNotFoundException


class TaskORM(models.Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    description = fields.CharField(max_length=1000)
    status = fields.CharEnumField(TaskStatus)
    assignee = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

class ORMTaskRepo(TaskRepo):
        async def get_task(self, id: str) -> Task:
            try:
                task_orm = await TaskORM.get(id=self.task_id(id))
            except DoesNotExist:
                raise TaskNotFoundException(f"Task {self.task_id(id)} not found")
            return Task(
                id=f"POPUG-{task_orm.id}",
                title=task_orm.title,
                description=task_orm.description,
                status=task_orm.status,
                assignee=task_orm.assignee,
            )
            
    
        async def list_tasks(self, task_filter: Optional[TaskFilter] = None) -> List[Task]:
            tasks = await TaskORM.all()
            return [
                Task(
                    id=f"POPUG-{task.id}",
                    title=task.title,
                    description=task.description,
                    status=task.status,
                    assignee=task.assignee,
                ) for task in tasks if task_filter(task)
            ]

        async def create_task(self, title: str, assignee: str, description: str) -> Task:
            task = await TaskORM.create(
                title=title,
                assignee=assignee,
                description=description,
                status=TaskStatus.IN_PROGRESS,
            )
            task = Task(
                id=f"POPUG-{task.id}",
                title=title,
                assignee=assignee, 
                description=description,
                status=TaskStatus.IN_PROGRESS,
                )
            return task
    
        async def update_task(self, id: str, upd: TaskORM) -> TaskORM:
            try:
                task_orm = await TaskORM.get(id=self.task_id(id))
            except DoesNotExist:
                raise TaskNotFoundException(f"Task {self.task_id(id)} not found")
            
            task_orm.assignee = upd.assignee
            task_orm.title = upd.title
            task_orm.description = upd.description
            task_orm.status = upd.status
            await task_orm.save()

            return Task(
                id=f"POPUG-{task_orm.id}",
                title=task_orm.title,
                assignee=task_orm.assignee, 
                description=task_orm.description,
                status=task_orm.status,
                )

        @classmethod
        def task_id(cls, task_id: str) -> int:
            return int(task_id.split("-")[1])

@lru_cache()
async def get_task_repo():
    return ORMTaskRepo()
    