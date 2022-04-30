from database.db import *
from utils.requests import *
from utils.logger import get_logger
from utils.constants import DAYS_ENG, DAYS_MATCHING, PARITY_RU, PARITY_MATCHING
from fastapi import FastAPI
from transliterate import detect_language, translit


logger = get_logger(__name__)

app = FastAPI()


@app.get('/schedule/')
async def get_schedule(id: int, stream_group: str, parity: str, day: str | None = None) -> dict:
    '''GET запрос на получение расписания по группе, четности недели и дню недели'''
    stream_group = translit(stream_group, language_code='ru', reversed=True) if detect_language(stream_group) is not None else stream_group
    day = DAYS_MATCHING.get(day) if day not in DAYS_ENG else day
    parity = PARITY_MATCHING.get(parity) if parity not in PARITY_RU else parity
    schedule_dict: dict = await db_get_schedule(id=id, stream_group=stream_group, parity=parity, day=day)
    return schedule_dict


@app.post('/change-schedule-headman/')
async def change_schedule_headman(request: ChangeScheduleHeadman) -> dict:
    '''POST запрос на запись изменений в расписании старосты'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_headman_schedule(stream_group, day, parity, request.pair_number, request.changes)
    return {"ok": True}


@app.post('/change-schedule-personal/')
async def change_schedule_personal(request: ChangeSchedulePersonal) -> dict:
    '''POST запрос на запись изменений в расписании персональном'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_personal_schedule(request.id, stream_group, day, parity, request.pair_number, request.changes)
    return {"ok": True}


@app.post('/remove-pair-headman/')
async def remove_pair_headman(request: RemovePairHeadman) -> dict:
    '''POST запрос на удаление пары из расписания'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_headman_schedule(stream_group, day, parity, request.pair_number)
    return {"ok": True}


@app.post('/remove-pair-personal/')
async def remove_pair_personal(request: RemovePairPersonal) -> dict:
    '''POST запрос на удаление пары из расписания'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_personal_schedule(request.id, stream_group, day, parity, request.pair_number)
    return {"ok": True}


@app.post('/reset-schedule-headman/')
async def reset_schedule_headman(request: ResetScheduleHeadman) -> dict:
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_reset_day_headman(stream_group, day, parity)
    return {"ok": True}


@app.post('/reset-schedule-personal/')
async def reset_schedule_personal(request: ResetSchedulePersonal) -> dict:
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_reset_day_personal(request.id, stream_group, day, parity)
    return {"ok": True}


@app.post('/add-annotation-headman/')
async def add_annotation_headman(request: AddAnnotationHeadman) -> dict:
    '''POST запрос на запись аннтоации ко дню определенной группы и четности недели'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_annotation_headman(stream_group, day, parity, request.annotation)
    return {"ok": True}


@app.post('/add-annotation-personal/')
async def add_annotation_personal(request: AddAnnotationPersonal) -> dict:
    '''POST запрос на запись аннтоации ко дню определенной группы и четности недели'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_set_annotation_personal(request.id, stream_group, day, parity, request.annotation)
    return {"ok": True}


@app.post('/remove-annotation-headman/')
async def remove_annotation_headman(request: RemoveAnnotationHeadman) -> dict:
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_remove_annotation_headman(stream_group, day, parity)
    return {"ok": True}


@app.post('/remove-annotation-personal/')
async def remove_annotation_personal(request: RemoveAnnotationPersonal) -> dict:
    '''POST запрос на сброс измененного расписания в первоначальное состояние'''
    stream_group = translit(request.stream_group, language_code='ru', reversed=True) if detect_language(request.stream_group) is not None else request.stream_group
    day = DAYS_MATCHING.get(request.day) if request.day not in DAYS_ENG else request.day
    parity = PARITY_MATCHING.get(request.parity) if request.parity not in PARITY_RU else request.parity
    await db_remove_annotation_personal(request.id, stream_group, day, parity)
    return {"ok": True}
