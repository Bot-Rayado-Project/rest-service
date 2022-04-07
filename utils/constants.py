import os


class NoneException(Exception):
    pass


USER = os.environ.get('DBUSER')
PASSWORD = os.environ.get('DBPASSWORD')
NAME = os.environ.get('DBNAME')
HOST = os.environ.get('DBHOST')

SQL_SELECT_SCHEDULE = "SELECT schedule FROM schedule_table WHERE streamgroup='{}' AND dayofweek = '{}' AND even='{}'"
#SQL_SELECT_FULL_SCHEDULE = 'SELECT schedule FROM schedule_table WHERE group={} AND even={}' ты блять сначала научись первый запрос нормально писать а потом блять в полное раписание лезь

if USER == None or PASSWORD == None or NAME == None or HOST == None:
    raise NoneException
