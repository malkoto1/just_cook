__author__ = 'Vojda'

from pymongo import MongoClient
from sources.utils.skeleton import User, Recipe
from sources.utils import utils


class Databaser(object):
    @classmethod
    def get_db(cls, db='just_cook', host='localhost', port=27017):
        client = MongoClient(host, port)
        return Databaser(client[db])

    @classmethod
    def delete_db(cls, db, host='localhost', port=27017):
        client = MongoClient(host, port)
        client.drop_database(db)

    def __init__(self, db):
        self.db = db

    def add_product(self, name):
        if not self.db.products.count({'name': name}) > 0:
            return self.db.products.insert_one({'name': name}).inserted_id

    def get_products(self):
        return [product['name'] for product in self.db.products.find()]

    def edit_product(self, old_name, new_name):
        self.db.products.update({'name': old_name}, {'name': new_name})

    def delete_product(self, name):
        self.db.products.remove({'name': name})

    def add_user(self, username, password, admin=False):
        if not self.db.users.count({'username': username}) > 0:
            return self.db.users.insert_one({'username': username,
                                        'password': password,
                                        'admin': admin}).inserted_id

    def edit_user(self, user):
        self.db.users.update({'username': user.username},
                        user.__dict__)

    def delete_user(self, username):
        self.db.users.remove({'username': username})

    def get_all_users(self):
        return [User.from_dict(user) for user in self.db.users.find()]

    def get_user(self, username):
        return self.db.users.find_one({'username': username})

    def is_user_valid(self, username, password):
        user = self.get_user(username)
        if user:
            if user['password'] == password:
                return True
        return False

    def add_recipe(self, recipe):
        recipe_dict = recipe.__dict__
        del recipe_dict['_id']
        return self.db.recipes.insert_one(recipe_dict).inserted_id

    def get_recipe(self, idd):
        return self.db.recipes.find_one({'_id': idd})

    def get_all_recipes(self):
        return [Recipe.from_dict(recipe) for recipe in self.db.recipes.find()]

    def edit_recipe(self, recipe):
        self.db.recipes.update({'_id': recipe._id},
                                recipe.__dict__)

    def delete_recipe(self, id):
        self.db.recipes.remove({'_id': id})

    def find_recipes(self, search_criteria):
        needed_recipes = []
        all_recipes = [Recipe.from_dict(recipe) for recipe in self.db.recipes.find()]
        for recipe in all_recipes:
            for key in search_criteria.keys():
                if all(x in getattr(recipe, key) for x in search_criteria[key]):
                    needed_recipes.append(recipe)

        return needed_recipes

    def add_cookie(self, hash, expires, username):
        self.db.cookies.insert_one({'Hash': hash, 'Alive_Until': expires, 'user':username})

    def get_cookie(self, hash):
        return self.db.cookies.find_one({'Hash': hash})

    def is_cookie_valid(self, hash):
        cookie = self.get_cookie(hash)
        if cookie and cookie['Alive_Until'] > utils.get_current_time():
            return True
        return False

    def remove_expired_cookies(self):
        cookies = self.db.cookies.find()
        now = utils.get_current_time()
        for cookie in cookies:
            if now > cookie['Alive_Until']:
                self.db.cookies.remove({'Hash':cookie['Hash']})

    def is_admin(self, hash):
        cookie = self.get_cookie(hash)
        user = self.get_user(cookie['user'])
        return user['admin']