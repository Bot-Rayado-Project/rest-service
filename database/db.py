import asyncpg
from utils.constants import SQL_SELECT_SCHEDULE


async def db_connect(user: str = 'postgres', password: str = 'admin', name: str = 'schedules', host: str = 'localhost'):
    connection = await asyncpg.connect(user=user, password=password, database=name, host=host)
    return connection

async def db_close(connection):
    await connection.close()

async def get_schedule_from_database(connection, group: str, day: str, even: bool):
    schedule = await connection.fetch(SQL_SELECT_SCHEDULE.format(group.lower(), day.lower(), even))
    if len(schedule) == 0:
        return "Empty"
    else:
        return dict(schedule)[0]

""" 
async def get_full_schedule_from_database(group: str, even: bool):
    conn = await db_connect()
    schedule = await conn.fetch(SQL_SELECT_FULL_SCHEDULE.format(group.lower(), even)) """