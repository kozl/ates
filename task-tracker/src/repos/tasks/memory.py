from functools import lru_cache
from typing import List, Optional

from repos.tasks.abstract import TaskRepo, TaskFilter
from repos.tasks.exceptions import TaskNotFoundException
from repos.tasks.models import ORMTask, TaskStatus

class InMemoryTaskRepo(TaskRepo):
    
        def __init__(self):
            self.tasks = []
            self.tasks_dict = {}
            self.latest_task_id = 1
    
        def get_task(self, task_id: str) -> ORMTask:
            try:
                idx = self.tasks_dict[task_id]
                return self.tasks[idx]
            except KeyError:
                raise TaskNotFoundException(f"Task {task_id} not found")
    
        def list_tasks(self, task_filter: Optional[TaskFilter] = None) -> List[ORMTask]:
            return list(filter(task_filter, self.tasks))

        def create_task(self, assignee: str, description: str) -> ORMTask:
            task_id = f"POPUG-{self.latest_task_id}"
            task = ORMTask(
                id=task_id,
                assignee=assignee, 
                description=description,
                status=TaskStatus.IN_PROGRESS,
                )
            idx = len(self.tasks)
            self.tasks.append(task)
            self.tasks_dict[task_id] = idx
            self.latest_task_id += 1

            return task
    
        def update_task(self, task_id: str, upd: ORMTask) -> ORMTask:
            try:
                idx = self.tasks_dict[task_id]
                task = self.tasks[idx]
            except KeyError:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            task.assignee = upd.assignee
            task.description = upd.description
            task.status = upd.status

            return task

@lru_cache()
def get_task_repo():
    return InMemoryTaskRepo()