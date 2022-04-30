from database.db import *
from utils.requests import *
from utils.logger import get_logger
from utils.constants import DAYS_ENG, DAYS_MATCHING, PARITY_RU, PARITY_MATCHING
from fastapi import FastAPI


logger = get_logger(__name__)

app = FastAPI()


@app.get('/schedule/')
async def get_schedule(id: int, stream_group: str, parity: str, day: str | None = None):
    '''GET запрос на получение расписания по группе, четности недели и дню недели'''
    day = DAYS_MATCHING.get(day) if day not in DAYS_ENG else day
    parity = PARITY_MATCHING.get(parity) if parity not in PARITY_RU else parity
    schedule_dict: dict = await db_get_schedule(id=id, stream_group=stream_group, parity=parity, day=day)
    return schedule_dict


@app.post('/change-schedule-headman/')
async def change_schedule_headman(request: ChangeScheduleHeadman):
    '''POST запрос на запись изменений в расписании старосты'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_headman_schedule(request.stream_group, day, parity, request.pair_number, request.changes)
    return {"ok": True}


@app.post('/change-schedule-personal/')
async def change_schedule_personal(request: ChangeSchedulePersonal):
    '''POST запрос на запись изменений в расписании персональном'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_personal_schedule(request.id, request.stream_group, day, parity, request.pair_number, request.changes)
    return {"ok": True}


@app.post('/remove-pair-headman/')
async def remove_pair_headman(request: RemovePairHeadman):
    '''POST запрос на удаление пары из расписания'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_headman_schedule(request.stream_group, day, parity, request.pair_number)
    return {"ok": True}


@app.post('/remove-pair-personal/')
async def remove_pair_personal(request: RemovePairPersonal):
    '''POST запрос на удаление пары из расписания'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_personal_schedule(request.id, request.stream_group, day, parity, request.pair_number)
    return {"ok": True}


@app.post('/reset-schedule-headman/')
async def reset_schedule_headman(request: ResetScheduleHeadman):
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_reset_day_headman(request.stream_group, day, parity)
    return {"ok": True}


@app.post('/reset-schedule-personal/')
async def reset_schedule_personal(request: ResetSchedulePersonal):
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_reset_day_personal(request.id, request.stream_group, day, parity)
    return {"ok": True}


@app.post('/add-annotation-headman/')
async def add_annotation_headman(request: AddAnnotationHeadman):
    '''POST запрос на запись аннтоации ко дню определенной группы и четности недели'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_annotation_headman(request.stream_group, day, parity, request.annotation)
    return {"ok": True}


@app.post('/add-annotation-personal/')
async def add_annotation_personal(request: AddAnnotationPersonal):
    '''POST запрос на запись аннтоации ко дню определенной группы и четности недели'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_annotation_personal(request.id, request.stream_group, day, parity, request.annotation)
    return {"ok": True}


@app.post('/remove-annotation-headman/')
async def remove_annotation_headman(request: RemoveAnnotationHeadman):
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_remove_annotation_headman(request.stream_group, day, parity)
    return {"ok": True}


@app.post('/remove-annotation-personal/')
async def remove_annotation_personal(request: RemoveAnnotationPersonal):
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_remove_annotation_personal(request.id, request.stream_group, day, parity)
    return {"ok": True}
