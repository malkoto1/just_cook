__author__ = 'Vojda'

import unittest
from sources.utils import db_utils


DB_NAME = 'test'


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.db = db_utils.get_db(DB_NAME)

    def tearDown(self):
        db_utils.delete_db(DB_NAME)

