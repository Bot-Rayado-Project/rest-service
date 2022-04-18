import os
from pydantic import BaseModel


class BaseHeadmanRequest(BaseModel):
    week: str
    dayofweek: str
    group: str


class ChangePair(BaseHeadmanRequest):
    pair: int
    changes: str


class AddAnnotation(BaseHeadmanRequest):
    annotation: str


class RemovePair(BaseHeadmanRequest):
    pair: int


class ResetSchedule(BaseHeadmanRequest):
    ...


class RemoveAnnotation(BaseHeadmanRequest):
    ...


class NoneException(Exception):
    pass


DBUSER = os.environ.get('DBUSER')
DBNAME = os.environ.get('DBNAME')
DBHOST = os.environ.get('DBHOST')
DBPASSWORD = os.environ.get('DBPASSWORD')
EADRESS = os.environ.get('EADRESS')
EPASSWORD = os.environ.get('EPASSWORD')
DEBUG = os.environ.get('DEBUG') or False

SQL_SELECT_SCHEDULE = "SELECT schedule FROM schedule_table WHERE streamgroup='{}' AND dayofweek = '{}' AND even='{}'"
SQL_SELECT_FULL_SCHEDULE = "SELECT schedule FROM schedule_table WHERE streamgroup='{}' AND even='{}'"

DAYS_ENG = ['ponedelnik', 'vtornik', 'sreda', 'chetverg', 'pjatnitsa', 'subbota']

if DBUSER == None or DBPASSWORD == None or DBNAME == None or DBHOST == None:
    raise NoneException

TIME = {
    1: '9:30 - 11:05\n',
    2: '11:20 - 12:55\n',
    3: '13:10 - 14:45\n',
    4: '15:25 - 17:00\n',
    5: '17:15 - 18:50\n'
}
