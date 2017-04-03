from api.ploneapi import PloneApi
from database.database import Database
from database.models.analysisprofile import AnalysisProfile
from database.models.sampletype import SampleType
from database.models.disease import Disease
from database.models.country import Country
from database.models.district import District
from database.models.syncjob import SyncJob
from database.models.patient import Patient
from database.models.analysisrequest import AnalysisRequest
from utils.config import intervals
import threading
import time


class Run:
    """
    The Main Class. To start Sync App, it is enough to initiate instance of
    this class...
    """
    def __init__(self):
        self.api = PloneApi()
        self.db = Database()
        # We are running different methods for each content type because time
        # intervals of diverse content type can differ.
        # self.processAnalysisProfiles()
        # self.processSampleTypes()
        # self.processDiseases()
        # self.processCountries()
        # self.processDistricts()
        # self.processForms()
        # patient = Patient('test', 'test', 'test', time.time(),
        # '12346', '123@3321.com', 'client-1116')
        # result = self.api.createPatient(patient)
        # print result
        print self.api.createAR()


    def processCountries(self):
        try:
            imported = 0
            db_codes = self.db.get_codes('countries')
            api_countries = self.api.getCountries().get('rows')
            new_countries = [Country(code=co['Code'],
                                     title=co['Country'])
                             for co in api_countries
                             if co['Code'] not in db_codes]
            imported = len(new_countries)
            for c in new_countries:
                self.db.insert('countries', c.get_db_format())
            message = str(imported) + ' New Country imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'Country')
        threading.Timer(intervals['country'], self.processCountries).start()

    def processDistricts(self):
        try:
            imported = 0
            db_titles = self.db.get_districts()
            api_districts = self.api.getDistricts()
            new_districts = [District(cocode=d[0],
                                      title=d[1])
                             for d in api_districts
                             if d[1] not in db_titles]
            imported = len(new_districts)
            for d in new_districts:
                self.db.insert('districts', d.get_db_format())
            message = str(imported) + ' New District imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'District')
        threading.Timer(intervals['district'], self.processDistricts).start()

    def processAnalysisProfiles(self):
        try:
            imported = 0
            db_uids = self.db.get_uids('analysisprofiles')
            api_profiles = self.api.getContents('AnalysisProfile').get('items')
            new_profiles = [AnalysisProfile(uid=prof['uid'],
                                            title=prof['title'])
                            for prof in api_profiles
                            if prof['uid'] not in db_uids]
            imported = len(new_profiles)
            for p in new_profiles:
                self.db.insert('analysisprofiles', p.get_db_format())
            message = str(imported) + ' New Profile imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'AnalysisProfile')
        threading.Timer(intervals['aprofile'],
                        self.processAnalysisProfiles).start()

    def processSampleTypes(self):
        try:
            imported = 0
            db_uids = self.db.get_uids('sampletypes')
            api_samtypes = self.api.getContents('SampleType').get('items')
            new_samtypes = [SampleType(uid=st['uid'],
                                       title=st['title'])
                            for st in api_samtypes
                            if st['uid'] not in db_uids]
            imported = len(new_samtypes)
            for st in new_samtypes:
                self.db.insert('sampletypes', st.get_db_format())
            message = str(imported) + ' New Sample Type imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'SampleType')
        threading.Timer(intervals['sampletype'],
                        self.processSampleTypes).start()

    def processDiseases(self):
        try:
            imported = 0
            db_uids = self.db.get_uids('diseases')
            api_diss = self.api.getContents('Disease').get('items')
            new_diseases = [Disease(uid=d['uid'],
                                    title=d['title'])
                            for d in api_diss
                            if d['uid'] not in db_uids]
            imported = len(new_diseases)
            for d in new_diseases:
                self.db.insert('diseases', d.get_db_format())
            message = str(imported) + ' New Disease imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'Disease')
        threading.Timer(intervals['disease'], self.processDiseases).start()

    def processForms(self):
        """
        This function gets all newly created IDSR forms and sends requests to
        API to create Patient and ARs. If API response is success then it
        updates Form's 'bika-status'.
        For each IDSR Form, 2 logs are inserted (one for Patient and one for
        AR).
        """
        try:
            forms = self.db.get_waiting_forms()
            for f in forms:
                p_result = self.api.createPatient(f.getPatient())
                if p_result['success']:
                    message = 'Patient Created. ID: '+p_result['obj_id']
                    status = 'Success'
                    self.insert_log(status, message,
                                    'Patient', f.getId())
                else:
                    message = p_result['message']
                    status = 'Fail'
                    self.insert_log(status, message,
                                    'Patient', f.getId())
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
            print message
            self.insert_log(status, message, 'AR & Patient')
        # threading.Timer(intervals['disease'], self.processForms).start()

    def insert_log(self, status, message, content_type, idsr_id=None):
        log = SyncJob(log_time=time.time(),
                      status=status,
                      message=message,
                      content_type=content_type
                      )
        if idsr_id:
            log.set_idsr_id(idsr_id)
        self.db.insert('syncjobs', log.get_db_format())


run = Run()
