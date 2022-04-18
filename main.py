from database.db import db_get_schedule, db_reset_schedule, db_set_custom_schedule, db_get_annotation, db_add_annotation, db_remove_annotation
from utils.logger import get_logger
from utils.constants import ChangePair, RemovePair, ResetSchedule, AddAnnotation, RemoveAnnotation, TIME
from fastapi import FastAPI


logger = get_logger(__name__)

app = FastAPI()


@app.get('/schedule/')
async def get_schedule(group: str, even: bool, day: str | None = None):
    '''GET запрос на получение расписания по группе, четности недели и дню недели'''
    schedule_dict: dict = await db_get_schedule(group=group, even=even, day=day)
    schedule_dict['annotation'] = await db_get_annotation(group=group, even=even, day=day)
    return schedule_dict


@app.post('/change-schedule/')
async def change_schedule(request: ChangePair):
    '''POST запрос на запись изменений в расписание'''
    current_schedule = (await db_get_schedule(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek))["schedule"].split('⸻⸻⸻⸻⸻\n')
    current_schedule[request.pair - 1] = TIME[request.pair] + request.changes
    schedule = ''
    del current_schedule[-1]
    for pair in current_schedule:
        schedule += pair + '⸻⸻⸻⸻⸻\n'
    await db_set_custom_schedule(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek, schedule=schedule)
    return {"ok": True}


@app.post('/remove-pair/')
async def remove_pair(request: RemovePair):
    '''POST запрос на удаление пары из расписания'''
    current_schedule = (await db_get_schedule(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek))["schedule"].split('⸻⸻⸻⸻⸻\n')
    current_schedule[request.pair - 1] = 'Пары нет\n'
    schedule = ''
    del current_schedule[-1]
    for pair in current_schedule:
        schedule += pair + '⸻⸻⸻⸻⸻\n'
    await db_set_custom_schedule(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek, schedule=schedule)
    return {"ok": True}


@app.delete('/reset-schedule/')
async def reset_schedule(request: ResetSchedule):
    '''DELETE запрос на сброс измененного расписания в первоначальное состояние'''
    await db_reset_schedule(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek)
    return {"ok": True}


@app.post('/add-annotation/')
async def add_annotation(request: AddAnnotation):
    '''POST запрос на запись аннтоации ко дню определенной группы и четности недели'''
    await db_add_annotation(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek, annotation=request.annotation)
    return {"ok": True}


@app.delete('/remove-annotation/')
async def remove_annotation(request: RemoveAnnotation):
    '''DELETE запрос на сброс измененного расписания в первоначальное состояние'''
    await db_remove_annotation(group=request.group, even=(True if request.week.lower() == 'четная' else False), day=request.dayofweek)
    return {"ok": True}
