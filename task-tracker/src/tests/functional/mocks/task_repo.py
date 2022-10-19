import os
import json
from functools import lru_cache

from repos.tasks.models import Task
from repos.tasks.memory import InMemoryTaskRepo

TESTDATA_PATH = os.path.join(os.path.dirname(__file__), '../testdata')

@lru_cache()
def get_task_repo():
    tasks_raw = json.load(open(os.path.join(TESTDATA_PATH, 'tasks.json')))
    tasks = [Task.from_dict(data=user) for user in tasks_raw]
    return InMemoryTaskRepo(initial_tasks=tasks)