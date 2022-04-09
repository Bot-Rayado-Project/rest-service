from utils.logger import get_logger
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
            logger.info(f'Successfully connected to database {name} to host {host} with user {user}')
            return connection
        except Exception as e:
            tries -= 1
            logger.error(f"Error connecting to database ({e}). Tries left: {tries}: {traceback.format_exc()}")
            await asyncio.sleep(0.33)
            if tries == 0:
                return None


async def db_close(connection: asyncpg.Connection) -> None:
    '''Закрывает подключение с БД'''
    try:
        await connection.close()
    except Exception as e:
        logger.error(f"Error closing database ({e}): {traceback.format_exc()}")
        await asyncio.sleep(0.33)


async def db_get_schedule(connection: asyncpg.Connection, group: str, dayofweek: str, even: bool) -> dict:
    '''Забирает расписание по запросу'''
    database_responce: list = await connection.fetch(f"SELECT schedule FROM schedule_table WHERE streamgroup='{group}' AND dayofweek = '{dayofweek}' AND even='{even}'")
    try:
        print(database_responce)
        print(dict(database_responce[0]))
        print(len(dict(database_responce[0])))
        _database_responce = dict(database_responce[0])
        return _database_responce
    except Exception:
        logger.error(f"Error in converting data to dict. {traceback.format_exc()}")
        return None
