import faust

app = faust.App('task-tracker', broker='kafka://localhost')

class UserCreated(faust.Record):
    login: str
    role: str

user_created_topic = app.topic('UserCreated', value_type=UserCreated)

@app.agent(user_created_topic)
async def process_user_created(user_created_events):
    async for user_created in user_created_events:
        print(user_created)