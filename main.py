from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database.db import db_get_schedule
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()


@app.get('/{group}/{dayofweek}/{even}/{fullweek}')
async def get_schedule(group: str, dayofweek: str, even: bool, fullweek: bool) -> JSONResponse:
    logger.info(f'Request for /{group}/{dayofweek}/{even}/{fullweek}')
    return await db_get_schedule(group, dayofweek, even, fullweek)
