import asyncpg

SQL_SELECT = 'SELECT schedule FROM schedule_table WHERE group={} AND dayofweek = {} AND even={}'

async def get_schedule_from_database(group: str, day: str, even: bool):
    conn = await asyncpg.connect(user='postgres', password='admin', database='schedules', host='localhost')
    schedule = await conn.fetch(SQL_SELECT.format(group.lower(), day.lower(), even))
    await conn.close()
    return schedule