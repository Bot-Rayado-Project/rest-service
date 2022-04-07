import asyncpg
from utils.constants import SQL_SELECT_SCHEDULE
from utils.constants import USER, PASSWORD, HOST, NAME

async def db_connect(user: str, password: str, name: str, host: str):
    conn = await asyncpg.connect(user=user, password=password, database=name, host=host)
    return conn


async def get_schedule_from_database(group: str, day: str, even: bool):
    conn = await db_connect(USER, PASSWORD, HOST, NAME)
    schedule = await conn.fetch(SQL_SELECT_SCHEDULE.format(group.lower(), day.lower(), even))
    await conn.close()
    return schedule

""" 
async def get_full_schedule_from_database(group: str, even: bool):
    conn = await db_connect()
    schedule = await conn.fetch(SQL_SELECT_FULL_SCHEDULE.format(group.lower(), even)) """