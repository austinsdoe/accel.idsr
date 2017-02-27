from ConfigParser import ConfigParser
from pymongo import MongoClient
from idsr import IDSR

class Database(object):

    _db = None

    def connect(self, config):
        host = config.get('database', 'host')
        port = config.getint('database', 'port')
        name = config.get('database', 'name')

        # Is auth required?
        username = None
        password = None
        if config.has_option('database', 'user'):
            username = cfg.get('database', 'user')

        if config.has_option('database', 'password'):
            password = cfg.get('database', 'password')

        client = MongoClient(host, port)
        self._db = client[name]
        if username and password:
            if self._db.authenticate(username, password):
                self._db = None
        return self._db

    def get_db(self):
        return self._db

    def add_idsr_partial_full(self, idsr_data):
        self._db.partialidsr.update_one(
            {'_id': idsr_data['patient_record_id']},
            {"$set": idsr_data},
            upsert=False)

    def add_idsr(self, idsr_data):
        self._db.partialidsr.insert(self.idsr_load(idsr_data))

    def get_partial_idsr(self):
        partially_filled = self._db.partialidsr.find({'totally_filled': 'False'})
        return partially_filled

    def get_document_by_id(self, idsr_data):
        doc = self._db.partialidsr.find({'_id': idsr_data['patient_record_id']})
        return doc

    def idsr_load(self, idsr_data):
        idsr = IDSR().idsr_dict
        idsr.update(idsr_data)
        return idsr
