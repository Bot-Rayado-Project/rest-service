import typing
from utils.logger import get_logger
from utils.constants import DBUSER, DBPASSWORD, DBHOST, DBNAME, DAYS_ENG
from fastapi import HTTPException
import asyncpg
import asyncio
import traceback

logger = get_logger(__name__)


async def db_connect(user: str, password: str, name: str, host: str) -> asyncpg.Connection | None:
    '''Выполняет подключение к базе данных. В случае ошибки подключение выполняет еще одну попытку. Всего попыток 5.
    В случае последней неудачи возвращает None, иначе - asyncpg.Connection'''
    tries = 5
    while True:
        try:
            connection = await asyncpg.connect(user=user, password=password, database=name, host=host)
            if tries != 5:
                logger.info(f'Successfully connected to database {name} to host {host} with user {user}')
            return connection
        except Exception as e:
            tries -= 1
            logger.error(f"Error connecting to database ({e}). Tries left: {tries}")
            await asyncio.sleep(0.33)
            if tries == 0:
                logger.error(f"Error connecting to database: {traceback.format_exc()}")
                return None


async def db_close(connection: asyncpg.Connection) -> None:
    '''Закрывает подключение с БД'''
    try:
        await connection.close()
    except Exception as e:
        logger.error(f"Error closing database ({e}): {traceback.format_exc()}")
        await asyncio.sleep(0.33)


async def db_get_schedule(group: str, even: bool, day: typing.Optional[str] = None, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Забирает расписание по запросу. При запросе на полную неделю обязано вернуть 6 строк'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    if day is not None:
        '''Получаем сначала измененное расписание. Если нет, то получаем стандартное'''
        database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table_customized WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
        if len(database_responce) == 0:
            database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    else:
        database_responce: list = []
        for _day in DAYS_ENG:
            _database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table_customized WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
            if len(_database_responce) == 0:
                _database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table WHERE streamgroup='{group}' AND dayofweek = '{_day}' AND even='{even}'")
                if len(_database_responce) == 0:
                    await db_close(connection)
                    raise HTTPException(status_code=404, detail=f"Schedule for {_day} not found")
            database_responce.append(dict(schedule=dict(_database_responce[0])['schedule']))
    if len(database_responce) == 0:
        await db_close(connection)
        raise HTTPException(status_code=404, detail="Schedule not found")
    await db_close(connection)
    return dict(database_responce[0]) if day is not None else dict(schedule=database_responce)


async def db_set_custom_schedule(group: str, even: bool, day: str, schedule: str, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Забирает расписание по запросу. При запросе на полную неделю обязано вернуть 6 строк'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table_customized WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    if len(database_responce) == 0:
        await connection.fetchrow(f"INSERT INTO schedule_table_customized VALUES('{group}','{day}','{schedule}',{even});")
    else:
        await connection.fetchrow(f"UPDATE schedule_table_customized SET schedule = '{schedule}' WHERE streamgroup = '{group}' AND dayofweek = '{day}' AND even = '{even}';")


async def db_reset_schedule(group: str, even: bool, day: str, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Забирает расписание по запросу. При запросе на полную неделю обязано вернуть 6 строк'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table_customized WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    if len(database_responce) == 0:
        pass
    else:
        await connection.fetchrow(f"DELETE FROM schedule_table_customized WHERE streamgroup = '{group}' AND dayofweek = '{day}' AND even = '{even}';")


async def db_get_annotation(group: str, even: bool, day: typing.Optional[str] = None, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Забирает аннотацию по группе, четности, дню'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    if day is not None:
        database_responce: list = await connection.fetch(f"SELECT annotation FROM schedule_table_annotations WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    else:
        database_responce: list = []
        for _day in DAYS_ENG:
            _database_responce: list = await connection.fetch(f"SELECT annotation FROM schedule_table_annotations WHERE streamgroup='{group}' AND dayofweek = '{_day}' AND even='{even}'")
            if len(_database_responce) != 0:
                database_responce.append(dict(annotation=dict(_database_responce[0])['annotation']))
            else:
                database_responce.append(dict(annotation="No annotation found"))
    if len(database_responce) == 0:
        return "No annotation found"
    return database_responce[0]['annotation'] if day is not None else database_responce


async def db_add_annotation(group: str, even: bool, day: str, annotation: str, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Записывает аннотацию по группе, четности, дню'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    database_responce: list = await connection.fetch(f"SELECT annotation FROM schedule_table_annotations WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    if len(database_responce) == 0:
        await connection.fetchrow(f"INSERT INTO schedule_table_annotations VALUES('{group}','{day}','{annotation}',{even});")
    else:
        await connection.fetchrow(f"UPDATE schedule_table_annotations SET annotation = '{annotation}' WHERE streamgroup = '{group}' AND dayofweek = '{day}' AND even = '{even}';")


async def db_remove_annotation(group: str, even: bool, day: str, connection: typing.Optional[asyncpg.Connection] = None) -> dict:
    '''Удаляет аннотацию по запросу группы, четности, дне'''
    connection = connection or await db_connect(DBUSER, DBPASSWORD, DBNAME, DBHOST)
    database_responce: list = await connection.fetch(f"SELECT annotation FROM schedule_table_annotations WHERE streamgroup='{group}' AND dayofweek = '{day}' AND even='{even}'")
    if len(database_responce) == 0:
        pass
    else:
        await connection.fetchrow(f"DELETE FROM schedule_table_annotations WHERE streamgroup = '{group}' AND dayofweek = '{day}' AND even = '{even}';")
