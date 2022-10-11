import faust
from tortoise import Tortoise, run_async

from core.config import DB_URL, KAFKA_BROKER_URL
from repos.users.orm import UserORM

app = faust.App('task-tracker', broker=KAFKA_BROKER_URL)

class UserCreated(faust.Record, serializer='json'):
    login: str
    role: str

user_created_topic = app.topic('auth.events', value_type=UserCreated)

@app.agent(user_created_topic)
async def process_user_created(user_created_events):
    async for user_created in user_created_events:
        UserORM.create(login=user_created.login, role=user_created.role)

async def main():
    await Tortoise.init(db_url=DB_URL, modules={"models": ["repos.tasks.orm", "repos.users.orm"]})
    await app.main()

if __name__ == '__main__':

    app.main()