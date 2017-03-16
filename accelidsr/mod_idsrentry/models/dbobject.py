from accelidsr import db
from accelidsr.mod_idsrentry.models import fetch_by_id
from bson import ObjectId
import bson

class MongoDbBaseObject(object):

    _collection = ''
    _dict = { }

    def __init__(self, id=None):
        if id:
            self._dict['id'] = id

    def getCollection(self):
        return self._collection

    def update(self, data):
        self._dict.update(data)

    def set(self, key, val):
        self._dict[key] = val

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def getId(self):
        return self._dict.get('_id', None)

    def getDict(self):
        return self._dict
