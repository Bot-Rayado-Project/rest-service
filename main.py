from fastapi import FastAPI
from database.db import db_connect, db_close, db_get_schedule
from utils.constants import USER, PASSWORD, HOST, NAME
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()


@app.get('/{group}/{dayofweek}/{even}/{week}', status_code=200)
async def get_schedule(group: str, dayofweek: str, even: bool, week: bool):
    logger.info(f'Request for /{group}/{dayofweek}/{even}/{week}')
    connection = await db_connect(USER, PASSWORD, NAME, HOST)
    message = await db_get_schedule(connection, group, dayofweek, even)
    await db_close(connection)
    if week:
        return {'schedule': 'Error'}
    else:
        return message
