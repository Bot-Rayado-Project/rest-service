from fastapi import FastAPI
from database.db import get_schedule_from_database, db_connect, db_close, get_full_schedule_from_database
from utils.constants import USER, PASSWORD, HOST, NAME

app = FastAPI()

@app.get('/{group}/{day}/{even}/{week}', status_code=200)
async def get_schedule(group: str, day: str, even: bool, week: bool):

    if week:
        connection = db_connect(USER, PASSWORD, NAME, HOST)
        message = get_full_schedule_from_database(connection, group, even)
        db_close(connection)
        return {'schedule' : message}
    else:
        connection = db_connect(USER, PASSWORD, NAME, HOST)
        message = get_schedule_from_database(connection, group, day, even)
        db_close(connection)
        return {'schedule': message[0]}



