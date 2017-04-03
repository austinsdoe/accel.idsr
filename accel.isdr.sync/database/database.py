from pymongo import MongoClient
from utils.config import settings
from models.patient import Patient
from models.idsrform import IDSRForm
from models.analysisrequest import AnalysisRequest


class Database:

    _db = None

    def __init__(self):
        print 'Initializing DB...'
        self.connect()

    def get_db(self):
        return self._db

    def connect(self):
        print 'Connecting to DB...'
        host = settings['db_host']
        port = settings['db_port']
        name = settings['db_name']
        client = MongoClient(host, port)
        self._db = client[name]

    def insert(self, collection, obj):
        self._db[collection].insert(obj)

    def get_uids(self, collection):
        """ Use this function to get uids from any collection """
        results = []
        if not collection:
            return results
        if self._db[collection].find().count() > 0:
            coll = self._db[collection].find()
            for c in coll:
                results.append(c.get('uid'))
        return results

    def get_codes(self, collection):
        # For now we use this function to get Country codes.
        results = []
        if not collection:
            return results
        if self._db[collection].find().count() > 0:
            coll = self._db[collection].find()
            for c in coll:
                results.append(c.get('code'))
        return results

    def get_districts(self):
        results = []
        coll = self._db['districts'].find()
        for c in coll:
            results.append(c.get('title'))
        return results

    def get_waiting_forms(self):
        idsr_forms = []
        coll = self._db['idsrform'].find({"idsr-status-a_1": "complete"})
        for c in coll:
            form_id = c['idobj']

            p_clientPatientId = c['patient_client_patientid']
            p_surname = c['patient_lastname']
            p_firstname = c['patient_firstname']
            p_birthDate = c['patient_dateofbirth']
            p_gender = c['patient_gender']
            p_phone = c['patient_phone_number']
            healthCareFacility = c['facility_code']
            patient = Patient(p_clientPatientId, p_surname, p_firstname,
                              p_birthDate, p_gender, p_phone,
                              healthCareFacility)

            ar = AnalysisRequest('Test')
            idsr_form = IDSRForm(form_id, patient, ar)
            idsr_forms.append(idsr_form)

        return idsr_forms
