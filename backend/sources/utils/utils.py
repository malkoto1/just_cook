__author__ = 'Vojda'

import sources.utils.db_utils as dbutils

def is_admin(hash):
    cookie = dbutils.get_cookie(hash)
    user = dbutils.get_user(cookie['user'])
    return user['admin']
