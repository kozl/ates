import logging
import logging.config

import faust
from tortoise import Tortoise, run_async

from core.config import DB_URL, KAFKA_BROKER_URL
from core.logger import LOGGING
from repos.users.orm import UserORM
from repos.users.models import UserRole

app = faust.App('task-tracker', broker=KAFKA_BROKER_URL)

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

class UserCreated(faust.Record, serializer='json'):
    login: str
    role: str

user_created_topic = app.topic('auth.UserCreated', value_type=UserCreated)

@app.task
async def init_orm():
    await Tortoise.init(db_url=DB_URL, modules={"models": ["repos.tasks.orm", "repos.users.orm"]})
    await Tortoise.generate_schemas()


@app.agent(user_created_topic)
async def process_user_created(user_created_events):
    async for user_created in user_created_events:
        logger.info(f"User created: {user_created.login}")
        await UserORM.create(login=user_created.login, role=UserRole(user_created.role))

if __name__ == '__main__':
    app.main()