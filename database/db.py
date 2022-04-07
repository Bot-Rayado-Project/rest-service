from debugpy import connect
import psycopg2
from utils.constants import SQL_SELECT_SCHEDULE, SQL_SELECT_FULL_SCHEDULE


def db_connect(user: str = 'postgres', password: str = 'admin', name: str = 'schedules', host: str = 'localhost'):
    connection = psycopg2.connect(user=user, password=password, dbname=name, host=host)
    return connection

def db_close(connection):
    connection.close()

def get_schedule_from_database(connection, group: str, day: str, even: bool):
    cursor = connection.cursor()
    cursor.execute(SQL_SELECT_SCHEDULE.format(group.lower(), day.lower(), even))
    schedule = cursor.fetchall()
    if len(schedule) == 0:
        return "Empty"
    else:
        return schedule[0]


async def get_full_schedule_from_database(connection, group: str, even: bool):
    cursor = connection.cursor()
    cursor.execute(SQL_SELECT_FULL_SCHEDULE.format(group.lower(), even))
    schedule = cursor.fetchall()
    if len(schedule) == 0:
        return "Empty"
    else:
        return schedule