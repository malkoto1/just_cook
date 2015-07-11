__author__ = 'Vojda'

class User:
    """
    This is the user class
    """

    @classmethod
    def from_dict(cls, object_dict):

        return User(object_dict['username'], object_dict['password'], object_dict['admin'])

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = password
        self.admin = admin

    def to_json(self):
        return "{}"


class Recipe:
    """
    Recipe class representing the recipes in the db
    """

    @classmethod
    def from_dict(cls, object_dict):
        return Recipe(object_dict['name'], object_dict['products'], object_dict['description'], object_dict['checked'], object_dict['_id'])

    def __init__(self, name, products, description, checked=False, id=None):
        self.name = name
        self.products = products
        self.description = description
        self.checked = checked
        self._id = id


class Cookie:
    """
    A cookie representation:
    {"hash": "SOME HASH",
    "Expires": miliseconds
    }
    """

    def __init__(self, hash, expires):
        self.hash = hash
        self.expires = expires