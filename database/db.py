import typing

from utils.logger import get_logger
from utils.constants import DBUSER, DBPASSWORD, DBHOST, DBNAME, DAYS_ENG, DBPORT, TIME
from database.dals import *
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logger = get_logger(__name__)


url = f"postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

engine = create_async_engine(url, future=True, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def db_get_schedule(id: int, stream_group: str, parity: bool, day: typing.Optional[str] = None) -> dict:
    '''Асинхронно обращается к базе данных и забирает оттуда расписание. При отсутствии дня выводит всю неделю.
    Если общее расписание оказывается пустым, вызывает 404 Not Found Exception
    Пример вывода:
{
    "shared_schedule": {
        "chetverg": "Не пустая строка"
    },
    "headman_schedule": {
        "chetverg": ""
    },
    "personal_schedule": {
        "chetverg": ""
    },
    "headman_annotation": {
        "chetverg": ""
    },
    "personal_annotation": {
        "chetverg": ""
    },
    "headman_changes": {
        "chetverg": {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": ""
        }
    },
    "personal_changes": {
        "chetverg": {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": ""
        }
    }
}'''
    async with async_session() as session:
        async with session.begin():
            if day is not None:
                shared_schedule_dal = SharedScheduleDAL(session)
                shared_schedule = await shared_schedule_dal.get_shared_schedule(stream_group, day, parity)
                if len(shared_schedule) == 0:
                    raise HTTPException(
                        status_code=404, detail="Schedule not found")

                if len(shared_schedule) != 1:
                    logger.error(
                        f'Length of shared_schedule does not equal to 1: {shared_schedule}')
                    raise Exception('Shared schedule != 1')
                else:
                    shared_schedule = shared_schedule[0]

                headman_schedule_dal = HeadmanScheduleDAL(session)
                headman_schedule = await headman_schedule_dal.get_headman_schedule(stream_group, day, parity)
                if len(headman_schedule) != 0:
                    headman_schedule = headman_schedule[0]
                else:
                    headman_schedule = ''

                personal_schedule_dal = PersonalScheduleDAL(session)
                personal_schedule = await personal_schedule_dal.get_personal_schedule(id, stream_group, day, parity)
                if len(personal_schedule) != 0:
                    personal_schedule = personal_schedule[0]
                else:
                    personal_schedule = ''

                headman_annotations_dal = HeadmanAnnotationsDAL(session)
                headman_annotation = await headman_annotations_dal.get_headman_annotation(stream_group, day, parity)
                if len(headman_annotation) != 0:
                    headman_annotation = headman_annotation[0]
                else:
                    headman_annotation = ''

                personal_annotations_dal = PersonalAnnotationsDAL(session)
                personal_annotation = await personal_annotations_dal.get_personal_annotation(id, stream_group, day, parity)
                if len(personal_annotation) != 0:
                    personal_annotation = personal_annotation[0]
                else:
                    personal_annotation = ''

                headman_changes_dal = HeadmanChangesDAL(session)
                headman_changes = await headman_changes_dal.get_all_headman_changes(stream_group, day, parity)
                if len(headman_changes) == 0:
                    headman_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                else:
                    _headman_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                    headman_changes_pair_numbers = await headman_changes_dal.get_all_headman_changes_pair_numbers(stream_group, day, parity)
                    for i in range(len(headman_changes)):
                        _headman_changes[headman_changes_pair_numbers[i]
                                         ] = headman_changes[i]
                    headman_changes = _headman_changes

                personal_changes_dal = PersonalChangesDAL(session)
                personal_changes = await personal_changes_dal.get_all_personal_changes(id, stream_group, day, parity)
                if len(personal_changes) == 0:
                    personal_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                else:
                    _personal_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                    personal_changes_pair_numbers = await personal_changes_dal.get_all_personal_changes_pair_numbers(id, stream_group, day, parity)
                    for i in range(len(personal_changes)):
                        _personal_changes[personal_changes_pair_numbers[i]
                                          ] = personal_changes[i]
                    personal_changes = _personal_changes

                return {'shared_schedule': {day: shared_schedule},
                        'headman_schedule': {day: headman_schedule},
                        'personal_schedule': {day: personal_schedule},
                        'headman_annotation': {day: headman_annotation},
                        'personal_annotation': {day: personal_annotation},
                        'headman_changes': {day: headman_changes},
                        'personal_changes': {day: personal_changes}}

            else:
                shared_schedule = {}
                headman_schedule = {}
                personal_schedule = {}
                headman_annotation = {}
                personal_annotation = {}
                headman_changes = {}
                personal_changes = {}

                shared_schedule_dal = SharedScheduleDAL(session)
                headman_schedule_dal = HeadmanScheduleDAL(session)
                personal_schedule_dal = PersonalScheduleDAL(session)
                headman_annotations_dal = HeadmanAnnotationsDAL(session)
                personal_annotations_dal = PersonalAnnotationsDAL(session)
                headman_changes_dal = HeadmanChangesDAL(session)
                personal_changes_dal = PersonalChangesDAL(session)

                for _day in DAYS_ENG:

                    _shared_schedule = await shared_schedule_dal.get_shared_schedule(stream_group, _day, parity)
                    if len(_shared_schedule) != 1:
                        logger.error(
                            f'Length of _shared_schedule does not equal to 1 (full week requested): {shared_schedule}')
                        raise Exception('Shared schedule != 1')
                    shared_schedule[_day] = _shared_schedule[0]

                    _headman_schedule = await headman_schedule_dal.get_headman_schedule(stream_group, _day, parity)
                    if len(_headman_schedule) != 0:
                        _headman_schedule = _headman_schedule[0]
                    else:
                        _headman_schedule = ''
                    headman_schedule[_day] = _headman_schedule

                    _personal_schedule = await personal_schedule_dal.get_personal_schedule(id, stream_group, _day, parity)
                    if len(_personal_schedule) != 0:
                        _personal_schedule = _personal_schedule[0]
                    else:
                        _personal_schedule = ''
                    personal_schedule[_day] = _personal_schedule

                    _headman_annotation = await headman_annotations_dal.get_headman_annotation(stream_group, _day, parity)
                    if len(_headman_annotation) != 0:
                        _headman_annotation = _headman_annotation[0]
                    else:
                        _headman_annotation = ''
                    headman_annotation[_day] = _headman_annotation

                    _personal_annotation = await personal_annotations_dal.get_personal_annotation(id, stream_group, _day, parity)
                    if len(_personal_annotation) != 0:
                        _personal_annotation = _personal_annotation[0]
                    else:
                        _personal_annotation = ''
                    personal_annotation[_day] = _personal_annotation

                    _headman_changes = await headman_changes_dal.get_all_headman_changes(stream_group, _day, parity)
                    if len(_headman_changes) == 0:
                        _headman_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                    else:
                        _headman_changes_ = {1: '', 2: '', 3: '', 4: '', 5: ''}
                        _headman_changes_pair_numbers = await headman_changes_dal.get_all_headman_changes_pair_numbers(stream_group, _day, parity)
                        for i in range(len(_headman_changes)):
                            _headman_changes_[
                                _headman_changes_pair_numbers[i]] = _headman_changes[i]
                        _headman_changes = _headman_changes_
                    headman_changes[_day] = _headman_changes

                    _personal_changes = await personal_changes_dal.get_all_personal_changes(id, stream_group, _day, parity)
                    if len(_personal_changes) == 0:
                        _personal_changes = {1: '', 2: '', 3: '', 4: '', 5: ''}
                    else:
                        _personal_changes_ = {
                            1: '', 2: '', 3: '', 4: '', 5: ''}
                        _personal_changes_pair_numbers = await personal_changes_dal.get_all_personal_changes_pair_numbers(id, stream_group, _day, parity)
                        for i in range(len(_personal_changes)):
                            _personal_changes_[
                                _personal_changes_pair_numbers[i]] = _personal_changes[i]
                        _personal_changes = _personal_changes_
                    personal_changes[_day] = _personal_changes

                return {'shared_schedule': shared_schedule,
                        'headman_schedule': headman_schedule,
                        'personal_schedule': personal_schedule,
                        'headman_annotation': headman_annotation,
                        'personal_annotation': personal_annotation,
                        'headman_changes': headman_changes,
                        'personal_changes': personal_changes}


async def db_set_headman_schedule(stream_group: str, day: str, parity: str, pair_number: int, changes: typing.Optional[str] = 'Пары нет') -> None:
    '''Создает либо обновляет расписание, изменненное старостой'''
    async with async_session() as session:
        async with session.begin():
            headman_schedule_dal = HeadmanScheduleDAL(session)
            headman_changes_dal = HeadmanChangesDAL(session)

            headman_schedule = await headman_schedule_dal.get_headman_schedule(stream_group, day, parity)
            if len(headman_schedule) == 0:
                shared_schedule_dal = SharedScheduleDAL(session)
                shared_schedule = await shared_schedule_dal.get_shared_schedule(stream_group, day, parity)
                compiled_schedule = await compile_schedule(shared_schedule, pair_number, changes)
                await headman_schedule_dal.create_headman_schedule(stream_group, day, parity, compiled_schedule)

                headman_changes = await headman_changes_dal.get_headman_changes(stream_group, day, parity, pair_number)
                if len(headman_changes) == 0:
                    await headman_changes_dal.create_headman_changes(stream_group, day, parity, pair_number, changes)
                else:
                    await headman_changes_dal.update_headman_changes(stream_group, day, parity, pair_number, changes)
            else:
                headman_schedule = await headman_schedule_dal.get_headman_schedule(stream_group, day, parity)
                compiled_schedule = await compile_schedule(headman_schedule, pair_number, changes)
                await headman_schedule_dal.update_headman_schedule(stream_group, day, parity, compiled_schedule)

                headman_changes = await headman_changes_dal.get_headman_changes(stream_group, day, parity, pair_number)
                if len(headman_changes) == 0:
                    await headman_changes_dal.create_headman_changes(stream_group, day, parity, pair_number, changes)
                else:
                    await headman_changes_dal.update_headman_changes(stream_group, day, parity, pair_number, changes)


async def db_set_personal_schedule(id: int, stream_group: str, day: str, parity: str, pair_number: int, changes: typing.Optional[str] = 'Пары нет') -> None:
    '''Создает либо обновляет расписание, изменненное персонально'''
    async with async_session() as session:
        async with session.begin():
            personal_schedule_dal = PersonalScheduleDAL(session)
            personal_changes_dal = PersonalChangesDAL(session)

            personal_schedule = await personal_schedule_dal.get_personal_schedule(id, stream_group, day, parity)
            if len(personal_schedule) == 0:
                shared_schedule_dal = SharedScheduleDAL(session)
                shared_schedule = await shared_schedule_dal.get_shared_schedule(stream_group, day, parity)
                compiled_schedule = await compile_schedule(shared_schedule, pair_number, changes)
                await personal_schedule_dal.create_personal_schedule(id, stream_group, day, parity, compiled_schedule)

                personal_changes = await personal_changes_dal.get_personal_changes(id, stream_group, day, parity, pair_number)
                if len(personal_changes) == 0:
                    await personal_changes_dal.create_personal_changes(id, stream_group, day, parity, pair_number, changes)
                else:
                    await personal_changes_dal.update_personal_changes(id, stream_group, day, parity, pair_number, changes)
            else:
                personal_schedule = await personal_schedule_dal.get_personal_schedule(id, stream_group, day, parity)
                compiled_schedule = await compile_schedule(personal_schedule, pair_number, changes)
                await personal_schedule_dal.update_personal_schedule(id, stream_group, day, parity, compiled_schedule)

                personal_changes = await personal_changes_dal.get_personal_changes(id, stream_group, day, parity, pair_number)
                if len(personal_changes) == 0:
                    await personal_changes_dal.create_personal_changes(id, stream_group, day, parity, pair_number, changes)
                else:
                    await personal_changes_dal.update_personal_changes(id, stream_group, day, parity, pair_number, changes)


async def compile_schedule(schedule: str, pair_number: int, changes: str) -> str:
    '''Принимает текущее расписание, номер пары для изменения и сами изменения. Заменяет пару
    на нужную строку и возвращает расписание в общем виде'''
    schedule = schedule[0].split('⸻⸻⸻⸻⸻\n')
    if changes == 'Пары нет':
        schedule[pair_number - 1] = changes + '\n'
    else:
        schedule[pair_number - 1] = TIME[pair_number] + changes + '\n'
    _schedule = ''
    del schedule[-1]
    for pair in schedule:
        _schedule += pair + '⸻⸻⸻⸻⸻\n'
    return _schedule


async def db_reset_day_headman(stream_group: str, day: str, parity: str) -> None:
    '''Удаляет все, связанное с запрашиваемым днем для старосты'''
    async with async_session() as session:
        async with session.begin():

            # Удаление изменений старосты
            headman_schedule_dal = HeadmanScheduleDAL(session)
            await headman_schedule_dal.delete_headman_schedule(stream_group, day, parity)

            # Удаление аннотаций старосты
            headman_annotations_dal = HeadmanAnnotationsDAL(session)
            await headman_annotations_dal.delete_headman_annotation(stream_group, day, parity)

            # Удаление изменений пар старосты
            headman_changes_dal = HeadmanChangesDAL(session)
            await headman_changes_dal.delete_all_headman_changes(stream_group, day, parity)


async def db_reset_day_personal(id: int, stream_group: str, day: str, parity: str) -> None:
    '''Удаляет все, связанное с запрашиваемым днем для персонального'''
    async with async_session() as session:
        async with session.begin():

            # Удаление изменений любого человека
            personal_schedule_dal = PersonalScheduleDAL(session)
            await personal_schedule_dal.delete_all_personal_schedule(id, stream_group, day, parity)

            # Удаление аннотаций любого человека
            personal_annotations_dal = PersonalAnnotationsDAL(session)
            await personal_annotations_dal.delete_all_personal_annotation(id, stream_group, day, parity)

            # Удаление изменений пар любого человека
            personal_changes_dal = PersonalChangesDAL(session)
            await personal_changes_dal.delete_all_personal_changes(id, stream_group, day, parity)


async def db_set_annotation_headman(stream_group: str, day: str, parity: str, annotation: str) -> None:
    '''Создает или обновляет аннотацию для старосты'''
    async with async_session() as session:
        async with session.begin():
            headman_annotations_dal = HeadmanAnnotationsDAL(session)
            headman_annotation = await headman_annotations_dal.get_headman_annotation(stream_group, day, parity)
            if len(headman_annotation) == 0:
                await headman_annotations_dal.create_headman_annotation(stream_group, day, parity, annotation)
            else:
                await headman_annotations_dal.update_headman_annotation(stream_group, day, parity, annotation)


async def db_set_annotation_personal(id: int, stream_group: str, day: str, parity: str, annotation: str) -> None:
    '''Создает или обновляет аннотацию для персонального'''
    async with async_session() as session:
        async with session.begin():
            personal_annotations_dal = PersonalAnnotationsDAL(session)
            personal_annotation = await personal_annotations_dal.get_personal_annotation(id, stream_group, day, parity)
            if len(personal_annotation) == 0:
                await personal_annotations_dal.create_personal_annotation(id, stream_group, day, parity, annotation)
            else:
                await personal_annotations_dal.update_personal_annotation(id, stream_group, day, parity, annotation)


async def db_remove_annotation_headman(stream_group: str, day: str, parity: str) -> None:
    '''Удаляет аннотацию старосты'''
    async with async_session() as session:
        async with session.begin():
            headman_annotations_dal = HeadmanAnnotationsDAL(session)
            await headman_annotations_dal.delete_headman_annotation(stream_group, day, parity)


async def db_remove_annotation_personal(id: int, stream_group: str, day: str, parity: str) -> None:
    '''Удаляет аннотацию персонального'''
    async with async_session() as session:
        async with session.begin():
            personal_annotations_dal = PersonalAnnotationsDAL(session)
            await personal_annotations_dal.delete_personal_annotation(id, stream_group, day, parity)
