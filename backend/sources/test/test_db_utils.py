__author__ = 'Vojda'

import unittest
from sources.utils import db_utils
from sources.utils.skeleton import User, Recipe


DB_NAME = 'test'

# User
USERNAME = 'Gosho'


PASSWORD = 'aPass'

#Recipe
RECIPE_NAME = 'NAME'


DESCRIPTION = 'description'


PRODUCTS = {'product1': '150gr', 'product2': 'kolko iskash'}
class TestStringMethods(unittest.TestCase):

    def _add_user(self, username=USERNAME, password=PASSWORD, admin=True):
        self.db_utils.add_user(username, password, admin)

    def _add_recipe(self, name, products, description='', checked=False):
        recipe = Recipe(name, products, description, checked)
        idd = self.db_utils.add_recipe(recipe)
        return idd

    def setUp(self):
        self.db_utils = db_utils.Databaser.get_db(DB_NAME)

    def tearDown(self):
        db_utils.Databaser.delete_db(DB_NAME)

    def test_add_user(self):
        self._add_user()
        user = self.db_utils.get_user(USERNAME)

        self.assertEqual(USERNAME, user['username'])
        self.assertEqual(PASSWORD, user['password'])

    def test_add_multiple_users(self):
        self._add_user()
        self._add_user(USERNAME + 'ops')
        users = self.db_utils.get_all_users()

        self.assertEqual(2, len(users))

    def test_add_user_with_existing_username(self):
        self._add_user()
        self._add_user()
        users = self.db_utils.get_all_users()

        self.assertEqual(1, len(users))

    def test_edit_user(self):
        new_password = 'new_one'
        self._add_user()
        user = User(USERNAME, new_password, False)
        self.db_utils.edit_user(user)

        persisted_user = User.from_dict(self.db_utils.get_user(USERNAME))

        self.assertEqual(False, persisted_user.admin)
        self.assertEqual(new_password, persisted_user.password)

    def test_remove_users(self):
        self._add_user()
        self.db_utils.delete_user(USERNAME)

        self.assertEqual(0, len(self.db_utils.get_all_users()))

    def test_add_recipe(self):
        id = self._add_recipe(RECIPE_NAME, PRODUCTS, DESCRIPTION)
        recipe = self.db_utils.get_recipe(id)

        self.assertEqual(RECIPE_NAME, recipe['name'])
        self.assertEqual(PRODUCTS, recipe['products'])
        self.assertEqual(DESCRIPTION, recipe['description'])

    def test_remove_recipe(self):
        idd = self._add_recipe(RECIPE_NAME, PRODUCTS, DESCRIPTION)
        self.db_utils.delete_recipe(idd)

        self.assertEqual(0, len(self.db_utils.get_all_recipes()))

    def test_find_recipe(self):
        idd = self._add_recipe(RECIPE_NAME, PRODUCTS, DESCRIPTION)
        recipe = self.db_utils.find_recipes({'description': 'description'})[0]

        self.assertEqual(RECIPE_NAME, recipe.name)

    def test_add_cookie(self):
        self.db_utils.add_cookie('ajskhdkjashd', '1231231231312', USERNAME)
        cookie = self.db_utils.get_cookie('ajskhdkjashd')

        self.assertEqual(USERNAME, cookie['user'])