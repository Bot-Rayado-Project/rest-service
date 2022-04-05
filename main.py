from fastapi import FastAPI
from database.db import get_schedule_from_database

app = FastAPI()

@app.get('/{group}/{day}/{even}/{week}', status_code=200)
async def get_schedule(group: str, day: str, even: bool, week: bool):
    if week:
        schedule = []
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

        for day_from_database in days: 
            schedule.append(await get_schedule_from_database(group, day_from_database, even))

        return {'schedule': [{days[0]: schedule[0]}, {days[1]: schedule[1]}, {days[2]: schedule[2]},
                             {days[3]: schedule[3]}, {days[4]: schedule[4]}, {days[5]: schedule[5]}]}
    else:
        return {'schedule': await get_schedule_from_database(group, day, even)}



