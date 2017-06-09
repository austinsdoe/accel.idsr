from accelidsr import db
from accelidsr.mod_idsrentry.models import find_all
from accelidsr.mod_idsrentry.models.dbobject import MongoDbBaseObject
from bson import ObjectId
import bson


_collection = 'syncjobs'


class ErrorLog(MongoDbBaseObject):
    """
    Object class to show Error Logs from Sync App.
    """

    @staticmethod
    def findAll(sort='desc'):
        outitems = []
        col = db.get_collection(_collection)
        sortorder = 1 if sort == 'asc' else -1
        docs = col.find({'status': 'Fail'}).sort('$natural', sortorder)
        return docs
