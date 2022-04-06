import asyncpg

SQL_SELECT_SCHEDULE = 'SELECT schedule FROM schedule_table WHERE group={} AND dayofweek = {} AND even={}'
SQL_SELECT_FULL_SCHEDULE = 'SELECT schedule FROM schedule_table WHERE group={} AND even={}'

async def db_connect():
    conn = await asyncpg.connect(user='postgres', password='postgres', database='schedules', host='localhost')
    return conn


async def get_schedule_from_database(group: str, day: str, even: bool):
    conn = await db_connect()
    schedule = await conn.fetch(SQL_SELECT_SCHEDULE.format(group.lower(), day.lower(), even))
    await conn.close()
    return schedule

""" 
async def get_full_schedule_from_database(group: str, even: bool):
    conn = await db_connect()
    schedule = await conn.fetch(SQL_SELECT_FULL_SCHEDULE.format(group.lower(), even)) """