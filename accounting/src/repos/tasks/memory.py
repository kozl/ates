from functools import lru_cache
from typing import List, Optional
from datetime import datetime

from repos.tasks.abstract import TaskRepo, TaskFilter
from repos.tasks.exceptions import TaskNotFoundException
from repos.tasks.models import Task, TaskStatus

class InMemoryTaskRepo(TaskRepo):
    
        def __init__(self, initial_tasks: Optional[List[Task]] = None) -> None:
            self.tasks = []
            self.tasks_dict = {}
            self.latest_task_id = 1
            for task in initial_tasks or []:
                idx = len(self.tasks)
                self.tasks.append(task)
                self.tasks_dict[task.id] = idx
                self.latest_task_id += 1
    
        async def get_task(self, task_id: str) -> Task:
            try:
                idx = self.tasks_dict[task_id]
                return self.tasks[idx]
            except KeyError:
                raise TaskNotFoundException(f"Task {task_id} not found")
    
        async def list_tasks(self, task_filter: Optional[TaskFilter] = None) -> List[Task]:
            return list(filter(task_filter, self.tasks))

        async def create_task(self, task_id: str, assignee: str, fee: int, reward: int) -> Task:
            task = Task(
                id=task_id,
                assignee=assignee, 
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status=TaskStatus.IN_PROGRESS,
                )
            idx = len(self.tasks)
            self.tasks.append(task)
            self.tasks_dict[task_id] = idx
            self.latest_task_id += 1

            return task
    
        async def assign_task(self, task_id: str, assignee: str) -> int:
            try:
                idx = self.tasks_dict[task_id]
            except KeyError:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            self.tasks[idx].assignee = assignee
            self.tasks[idx].updated_at = datetime.now()

            return self.tasks[idx]

        async def close_task(self, task_id: str) -> Task:
            try:
                idx = self.tasks_dict[task_id]
            except KeyError:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            self.tasks[idx].status = TaskStatus.CLOSED
            self.tasks[idx].updated_at = datetime.now()

            return self.tasks[idx]

@lru_cache()
def get_task_repo():
    return InMemoryTaskRepo()