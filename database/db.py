import asyncpg
import os


class NoneException(Exception):
    pass


USER = os.environ.get('DBUSER')
PASSWORD = os.environ.get('DBPASSWORD')
NAME = os.environ.get('DBNAME')
HOST = os.environ.get('DBHOST')

SQL_SELECT_SCHEDULE = 'SELECT schedule FROM schedule_table WHERE group={} AND dayofweek = {} AND even={}'
SQL_SELECT_FULL_SCHEDULE = 'SELECT schedule FROM schedule_table WHERE group={} AND even={}'

if USER == None or PASSWORD == None or NAME == None or HOST == None:
    raise NoneException


async def db_connect(user: str, password: str, name: str, host: str):
    conn = await asyncpg.connect(user=user, password=password, database=name, host=host)
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