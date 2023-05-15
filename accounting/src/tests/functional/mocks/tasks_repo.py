import os
import json
from functools import lru_cache

from repos.tasks.models import Task, TaskStatus
from repos.tasks.memory import InMemoryTaskRepo

@lru_cache()
def get_task_repo():
    tasks = [
        Task(
            id="POPUG-1",
            assignee="ivan",
            created_at="2021-01-01T00:00:00",
            updated_at="2021-01-01T00:00:00",
            status=TaskStatus.IN_PROGRESS,
            fee=15,
            reward=23,
        ),
    ]
    return InMemoryTaskRepo(initial_tasks=tasks)