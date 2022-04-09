import os


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

if DBUSER == None or DBPASSWORD == None or DBNAME == None or DBHOST == None:
    raise NoneException
