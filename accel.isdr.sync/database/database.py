from pymongo import MongoClient
from utils.config import settings
from models.patient import Patient
from models.idsrform import IDSRForm
from models.contact import Contact
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
        # For now we use this function to get County codes.
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

    def update_status(self, form_id, status):
        result = db._db['idsrform'].update_one(
                    {"idobj": form_id},
                    {
                        "$set": {
                            "bika-status": status
                        }
                    }
                )

    def get_waiting_forms(self):
        """
        This function returns set of IDSR forms which are in_queue status.
        Each IDSR form object has a Patient and an AR objects created from
        Form's data.
        """
        idsr_forms = []
        query = {"idsr-status-a_1": "complete"}
        coll = self._db['idsrform'].find(query)
        for c in coll:
            form_id = c['idobj']
            facility_code = c['facility_code']

            # Setting up Patient
            p_clientPatientId = c['patient_client_patientid']
            p_surname = c['patient_lastname']
            p_firstname = c['patient_firstname']
            p_birthDate = c['patient_dateofbirth']
            p_gender = c['patient_gender']
            p_phone = c['patient_phone_number']
            patient = Patient(p_clientPatientId, p_surname, p_firstname,
                              p_birthDate, p_gender, p_phone,
                              facility_code)

            # Setting up Contact
            c_firstname = c['reporting_person_firstname']
            c_surname = c['reporting_person_lastname']
            contact = Contact(facility_code, c_firstname, c_surname)

            # Setting up AR
            ar_contact_uid = ''
            ar_cc_contact = ''
            ar_sampler_phone = c['sampler_phone']
            ar_case_id = c['case_id']
            ar_patient_record_id = c['patient_record_id']
            ar_reporting_health_facility = c['reporting_health_facility']
            ar_patient_uid = ''
            ar_sampling_date = c['date_sampled'].strftime("%y-%m-%d %H:%M")
            # TODO make sure that sample_type is UID
            ar_sample_type = c['sample_type']
            ar_analysis_specification = ''
            ar_analyses_requested = c['analyses_requested']
            ar_client_order_number = c['patient_record_id']

            ar = AnalysisRequest(ar_contact, ar_cc_contact, ar_sampler_phone,
                                 ar_case_id, ar_patient_record_id,
                                 ar_reporting_health_facility, ar_patient_uid,
                                 ar_sampling_date, ar_sample_type,
                                 ar_analysis_specification,
                                 ar_analyses_requested, ar_client_order_number)
            idsr_form = IDSRForm(form_id, patient, ar)
            idsr_forms.append(idsr_form)

        return idsr_forms
