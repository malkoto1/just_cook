__author__ = 'Vojda'

import requests
from bson.json_util import dumps, loads
from sources.utils.skeleton import Recipe

BASE_URL = 'http://localhost:8080/'

def get_all_recipes():
    r = requests.get(BASE_URL + 'recipes')
    recipes = loads(r.content.decode('utf-8'))
    return [Recipe.from_dict(recipe) for recipe in recipes]

def get_recipes(search_criteria):
    r = requests.get(BASE_URL + 'recipes', headers={'filter': dumps(search_criteria)})
    recipes = loads(r.content.decode('utf-8'))
    return [Recipe.from_dict(recipe) for recipe in recipes]

def remove_recipe(recipe):
    requests.delete(BASE_URL + 'recipes/?id=' + dumps(recipe._id))


def update_recipe(recipe):
    requests.put(BASE_URL + 'recipes', data=dumps(recipe))

get_all_recipes()
