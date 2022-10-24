import os
import json
from functools import lru_cache

from repos.users.models import User
from repos.users.memory import InMemoryUserRepo

TESTDATA_PATH = os.path.join(os.path.dirname(__file__), '../testdata')

@lru_cache()
def get_user_repo():
    users_raw = json.load(open(os.path.join(TESTDATA_PATH, 'users.json')))
    users = [User.from_dict(data=user) for user in users_raw]
    return InMemoryUserRepo(initial_users=users)