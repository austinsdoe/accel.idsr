from pymongo import MongoClient
from idsr import IDSR

class DBCONNECT(object):
    def get_db(self):
        client = MongoClient('localhost:27017')
        db = client.Idsr_Info
        return db

    def add_idsr_partial_full(self, idsr_data, db):

        db.partialidsr.update_one({
            '_id': idsr_data['patient_record_id']
        },
        {
            "$set": idsr_data
        }, upsert=False)

    def add_idsr(self, idsr_data, db):
        db.partialidsr.insert(self.idsr_load(idsr_data))

    def get_partial_idsr(self, db):
        partially_filled = db.partialidsr.find({'totally_filled': 'False'})
        return partially_filled

    def get_document_by_id(self, idsr_data, db):
        doc = db.partialidsr.find({'_id': idsr_data['patient_record_id']})
        return doc

    def idsr_load(self, idsr_data):
        idsr = IDSR().idsr_dict

        idsr.update(idsr_data)

        return idsr