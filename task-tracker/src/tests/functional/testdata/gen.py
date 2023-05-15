import os
import json
from datetime import datetime

from repos.tasks.models import Task, TaskStatus
from repos.users.models import User

from tests.functional.mocks.user_repo import TESTDATA_PATH

users = [
    User(login='accountant', role='accountant'),
    User(login='developer1', role='developer'),
    User(login='developer2', role='developer'),
    User(login='manager', role='manager'),
]

tasks = [
    Task(id="POPUG-1", created_at=datetime.now(), updated_at=datetime.now(), title="Create a new project", description="Create a new project", assignee=users[0].login, status=TaskStatus.IN_PROGRESS),
    Task(id="POPUG-2", created_at=datetime.now(), updated_at=datetime.now(), title="Make everything work", description="Make everything work", assignee=users[1].login, status=TaskStatus.IN_PROGRESS),
    Task(id="POPUG-3", created_at=datetime.now(), updated_at=datetime.now(), title="This is done", description="This is done", assignee=users[2].login, status=TaskStatus.CLOSED),
    Task(id="POPUG-4", created_at=datetime.now(), updated_at=datetime.now(), title="This is in progress", description="This is in progress", assignee=users[0].login, status=TaskStatus.IN_PROGRESS),
]

json.dump(users, open(os.path.join(TESTDATA_PATH, 'users.json'), 'w'), default=lambda x: x.__dict__, indent=4)
json.dump(tasks, open(os.path.join(TESTDATA_PATH, 'tasks.json'), 'w'), default=lambda x: x.to_dict(), indent=4)