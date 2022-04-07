from fastapi import FastAPI
from database.db import get_schedule_from_database

app = FastAPI()

@app.get('/{group}/{day}/{even}/{week}', status_code=200)
async def get_schedule(group: str, day: str, even: bool, week: bool):
    message = await get_schedule_from_database(group, day, even)
    if week:
        return {'schedule' : 'Error'}
    else:
        return {'schedule': str(message)}



