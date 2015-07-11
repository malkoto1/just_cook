__author__ = 'Vojda'

from pymongo import MongoClient
from sources.utils.skeleton import User, Recipe
from sources.utils import utils


def get_db(db='just_cook'):
    client = MongoClient('localhost', 27017)
    return client[db]


def delete_db(db):
    client = MongoClient('localhost', 27017)
    del client[db]


def add_product(name):
    db = get_db()
    if not db.products.count({'name': name}) > 0:
        return db.products.insert_one({'name': name}).inserted_id


def get_products():
    db = get_db()
    return [product['name'] for product in db.products.find()]


def edit_product(old_name, new_name):
    db = get_db()
    db.products.update({'name': old_name}, {'name': new_name})


def delete_product(name):
    db = get_db()
    db.products.remove({'name': name})


def add_user(username, password, admin=False):
    db = get_db()
    if not db.users.count({'username': username}) > 0:
        return db.users.insert_one({'username': username,
                                    'password': password,
                                    'admin': admin}).inserted_id


def edit_user(user):
    db = get_db()
    db.users.update({'username': user.username},
                    user.__dict__)


def delete_user(username):
    db = get_db()
    db.users.remove({'username': username})


def get_all_users():
    db = get_db()
    return [User.from_dict(user) for user in db.users.find()]


def get_user(username):
    db = get_db()
    return db.users.find_one({'username': username})


def is_user_valid(username, password):
    user = get_user(username)
    if user:
        if user['password'] == password:
            return True
    return False



def add_recipe(recipe):
    db = get_db()
    recipe_dict = recipe.__dict__
    del recipe_dict['id']
    return db.recipes.insert_one(recipe_dict).inserted_id


def get_all_recipes():
    db = get_db()
    return [Recipe.from_dict(recipe) for recipe in db.recipes.find()]


def edit_recipe(recipe):
    db = get_db()
    db.recipes.update({'_id': recipe.id},
                       recipe.__dict__)


def delete_recipe(id):
    db = get_db()
    db.recipes.remove({'_id': id})


def find_recipes(search_criteria):
    db = get_db()
    needed_recipes = []
    all_recipes = [Recipe.from_dict(recipe) for recipe in db.recipes.find()]
    for recipe in all_recipes:
        print(search_criteria)
        for key in search_criteria.keys():
            if all(x in getattr(recipe, key) for x in search_criteria[key]):
                needed_recipes.append(recipe)

    return needed_recipes


def add_cookie(hash, expires, username):
    db = get_db()
    db.cookies.insert_one({'Hash': hash, 'Alive_Until': expires, 'user':username})


def get_cookie(hash):
    db = get_db()
    return db.cookies.find_one({'Hash': hash})


def is_cookie_valid(hash):
    import time
    cookie = get_cookie(hash)
    if cookie and cookie['Alive_Until'] > utils.get_current_time():
        return True
    return False

def remove_expired_cookies():
    import time
    db = get_db()
    cookies = db.cookies.find()
    delete_cookies = []
    now = utils.get_current_time()
    for cookie in cookies:
        if now > cookie['Alive_Until']:
            db.cookies.remove({'Hash':cookie['Hash']})

