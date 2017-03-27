from accelidsr import db
from accelidsr.mod_idsrentry.models import find_all
from accelidsr.mod_idsrentry.models import fetch_by_id
from accelidsr.mod_idsrentry.models.dbobject import MongoDbBaseObject
from bson import ObjectId
import bson

class Idsr(MongoDbBaseObject):
    _collection = 'idsrform'

    @staticmethod
    def fetch(id):
        """
        Fetch an idsrform from the database and returns its Idsr object.
        Returns none if id is empty or no idsrform record found for the passed
        in id

        :param id: Unique identifier for the idsrform to be retrieved
        :type id: 12-byte input or a 24-character hex string
        :returns: The Idsr object that corresponds to the given id
        """
        doc = fetch_by_id(id, 'idsrform')
        if doc:
            idsr = Idsr(id)
            idsr.update(doc)
            return idsr
        return None

    @staticmethod
    def findAll(sort='desc'):
        outitems = []
        docs = find_all('idsrform', sort=sort)
        for doc in docs:
            idsr = Idsr(str(doc['_id']))
            idsr.update(doc)
            outitems.append(idsr)
        return outitems
