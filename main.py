from fastapi import FastAPI
from database.db import get_schedule_from_database, db_connect, db_close
from utils.constants import USER, PASSWORD, HOST, NAME

app = FastAPI()

@app.get('/{group}/{day}/{even}/{week}', status_code=200)
async def get_schedule(group: str, day: str, even: bool, week: bool):
    connection = await db_connect(USER, PASSWORD, HOST, NAME)
    message = await get_schedule_from_database(connection, group, day, even)
    await db_close(connection)
    if week:
        return {'schedule' : 'Error'}
    else:
        return {'schedule': str(message)}



