from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from dataclasses import dataclass

from repos.tasks.models import Task

TaskFilter = Callable[[Task], bool]


class TaskRepo(ABC):

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def list_tasks(self, filter: Optional[TaskFilter] = None) -> List[Task]:
        pass

    @abstractmethod
    def create_task(self, task_id: str, assignee: str, fee: int, reward: int) -> Task:
        pass

    @abstractmethod
    def assign_task(self, task_id: str, assignee: str) -> int:
        pass

    @abstractmethod
    def close_task(self, task_id: str) -> Task:
        pass