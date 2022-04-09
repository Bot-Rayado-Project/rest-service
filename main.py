from database.db import db_get_schedule
from utils.logger import get_logger
from fastapi import FastAPI
import typing

logger = get_logger(__name__)

app = FastAPI()


@app.get('/schedule/')
async def get_schedule(group: str, even: bool, day: typing.Optional[str] = None):
    return await db_get_schedule(group=group, even=even, day=day)
