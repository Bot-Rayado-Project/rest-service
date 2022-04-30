import os


class NoneException(Exception):
    pass


DBUSER = os.environ.get('DBUSER')
DBNAME = os.environ.get('DBNAME')
DBHOST = os.environ.get('DBHOST')
DBPORT = os.environ.get('DBPORT')
DBPASSWORD = os.environ.get('DBPASSWORD')
EADRESS = os.environ.get('EADRESS')
EPASSWORD = os.environ.get('EPASSWORD')
DEBUG = os.environ.get('DEBUG') or False

SQL_SELECT_SCHEDULE = "SELECT schedule FROM schedule_table WHERE streamgroup='{}' AND dayofweek = '{}' AND even='{}'"
SQL_SELECT_FULL_SCHEDULE = "SELECT schedule FROM schedule_table WHERE streamgroup='{}' AND even='{}'"

DAYS_ENG = ['ponedelnik', 'vtornik', 'sreda', 'chetverg', 'pjatnitsa', 'subbota']
PARITY_RU = ['четная', 'нечетная']

if DBUSER == None or DBPASSWORD == None or DBNAME == None or DBHOST == None:
    raise NoneException

TIME = {
    1: '9:30 - 11:05\n',
    2: '11:20 - 12:55\n',
    3: '13:10 - 14:45\n',
    4: '15:25 - 17:00\n',
    5: '17:15 - 18:50\n'
}

DAYS_MATCHING = {
    'понедельник': 'ponedelnik',
    'вторник': 'vtornik',
    'среда': 'sreda',
    'четверг': 'chetverg',
    'пятница': 'pjatnitsa',
    'суббота': 'subbota'
}

PARITY_MATCHING = {
    'chetnaja': 'четная',
    'nechetnaja': 'нечетная'
}
