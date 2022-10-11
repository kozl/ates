from typing import Optional, List

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist

from repos.tasks.models import TaskStatus, Task
from repos.tasks.abstract import TaskRepo, TaskFilter
from repos.tasks.exceptions import TaskNotFoundException


class TaskORM(models.Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=500)
    status = fields.CharEnumField(TaskStatus)
    assignee = fields.CharField(max_length=50)

class ORMTaskRepo(TaskRepo):
        async def get_task(self, task_id: str) -> Task:
            try:
                task_orm = await TaskORM.get(id=task_id)
            except DoesNotExist:
                raise TaskNotFoundException(f"Task {task_id} not found")
            return Task(
                id=f"POPUG-{task_orm.id}",
                description=task_orm.description,
                status=task_orm.status,
                assignee=task_orm.assignee,
            )
            
    
        async def list_tasks(self, task_filter: Optional[TaskFilter] = None) -> List[Task]:
            tasks = await TaskORM.all()
            return [
                Task(
                    id=f"POPUG-{task.id}",
                    description=task.description,
                    status=task.status,
                    assignee=task.assignee,
                ) for task in tasks if task_filter(task)
            ]

        async def create_task(self, assignee: str, description: str) -> Task:
            task = await TaskORM.create(
                assignee=assignee,
                description=description,
                status=TaskStatus.IN_PROGRESS,
            )
            task = Task(
                id=f"POPUG-{task.id}",
                assignee=assignee, 
                description=description,
                status=TaskStatus.IN_PROGRESS,
                )
            return task
    
        async def update_task(self, task_id: str, upd: TaskORM) -> TaskORM:
            try:
                task_orm = await TaskORM.get(id=task_id)
            except DoesNotExist:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            task_orm.assignee = upd.assignee
            task_orm.description = upd.description
            task_orm.status = upd.status
            await task_orm.save()

            return Task(
                id=f"POPUG-{task_orm.id}",
                assignee=task_orm.assignee, 
                description=task_orm.description,
                status=TaskStatus.IN_PROGRESS,
                )

async def get_task_repo():
    return ORMTaskRepo()
    