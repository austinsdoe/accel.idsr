from accelidsr import db
from accelidsr.mod_idsrentry.models import fetch_by_id
from bson import ObjectId
import bson

class MongoDbBaseObject(object):

    _collection = ''
    _dict = {}
    _created = None

    def __init__(self, id=None):
        self._dict = {}
        if id:
            self._dict['_id'] = id

    def getCollection(self):
        return self._collection

    def update(self, data):
        self._dict.update(data)
        if '_id' in data and isinstance(data['_id'], ObjectId):
            self._created = data['_id'].generation_time

    def set(self, key, val):
        self._dict[key] = val

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def getId(self):
        objid = self._dict.get('_id', None)
        return str(objid) if objid else None

    def created(self):
        return self._created

    def getDict(self):
        return self._dict
