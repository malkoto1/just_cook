__author__ = 'Vojda'

import sources.utils.db_utils as dbutils

ENCODING = 'utf-8'


def is_admin(hash):
    cookie = dbutils.get_cookie(hash)
    user = dbutils.get_user(cookie['user'])
    return user['admin']

def get_current_time():
    return int(round(time.time() * 1000))