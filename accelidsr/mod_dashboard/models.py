from accelidsr import db
from accelidsr.mod_idsrentry.models import find_all
from accelidsr.mod_idsrentry.models.dbobject import MongoDbBaseObject
from bson import ObjectId
import bson


class ErrorLog(MongoDbBaseObject):
    _collection = 'syncjobs'

    @staticmethod
    def findAll(sort='desc'):
        outitems = []
        docs = find_all(_collection, sort=sort)
        return outitems
