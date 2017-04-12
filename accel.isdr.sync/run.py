from api.ploneapi import PloneApi
from database.database import Database
from database.models.analysisprofile import AnalysisProfile
from database.models.sampletype import SampleType
from database.models.disease import Disease
from database.models.county import County
from database.models.district import District
from database.models.syncjob import SyncJob
from database.models.patient import Patient
from database.models.facility import Facility
from database.models.caseoutcome import CaseOutcome
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
        # intervals of diverse content types can differ.
        self.processAnalysisProfiles()
        self.processSampleTypes()
        self.processDiseases()
        self.processFacilities()
        self.processCounties()
        self.processDistricts()
        self.processForms()
        self.processOutcomes()
        # patient = Patient('test', 'test', 'test', time.time(),
        # '12346', '123@3321.com', 'client-1116')
        # result = self.api.create(patient)
        # print result
        # ar = AnalysisRequest('f250cdc98e274b3f9dda6a3b631339e8','','test2','','test4','f792373127944054bd1ff847015bb9b8','0f8dc35f79684ab09e6c48809f5e7cc5','2017-04-01 17:17',
        # '0a83e9783bc3435aaeafd9ccf9365430','','','test7',)
        # print self.api.createAR(ar)

    def processCounties(self):
        """
        Updates Counties (States/Provinces in Bika) from Bika Instace.
        """
        try:
            imported = 0
            db_codes = self.db.get_codes('counties')
            api_counties = self.api.getGeo('States')
            if not api_counties or len(api_counties) == 0:
                print '[WARN] No counties found in Bika'
            new_counties = [County(code=c[1],
                                   title=c[2])
                            for c in api_counties
                            if c[1] not in db_codes]
            imported = len(new_counties)
            for c in new_counties:
                self.db.insert('counties', c.get_db_format())
            message = str(imported) + ' Counties imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        # For Geo Objects we insert only one log when Sync Job is finished.
        self.insert_log(status, message, 'County')
        threading.Timer(intervals['county'], self.processCounties).start()

    def processDistricts(self):
        """
        Updates Districts from Bika Instace.
        """
        try:
            imported = 0
            db_titles = self.db.get_districts()
            api_districts = self.api.getGeo('Districts')
            if not api_districts or len(api_districts) == 0:
                print '[WARN] No districts found in Bika'
            new_districts = [District(cocode=d[1],
                                      title=d[2])
                             for d in api_districts
                             if d[2] not in db_titles]
            imported = len(new_districts)
            for d in new_districts:
                self.db.insert('districts', d.get_db_format())
            message = str(imported) + ' Districts imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        # For Geo Objects we insert only one log when Sync Job is finished.
        self.insert_log(status, message, 'District')
        threading.Timer(intervals['district'], self.processDistricts).start()

    def processAnalysisProfiles(self):
        """
        Updates AnalysisProfiles from Bika Instace.
        """
        try:
            imported = 0
            db_uids = self.db.get_uids('analysisprofiles')
            api_profiles = self.api.getContent('AnalysisProfile').get('items',{})
            if not api_profiles or len(api_profiles) == 0:
                print '[WARN] No Analysis Profiles found in Bika'
            new_profiles = [AnalysisProfile(uid=prof['uid'],
                                            title=prof['title'])
                            for prof in api_profiles
                            if prof['uid'] not in db_uids]
            imported = len(new_profiles)
            for p in new_profiles:
                self.db.insert('analysisprofiles', p.get_db_format())
            message = str(imported) + ' Analysis Profiles imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'AnalysisProfile')
        threading.Timer(intervals['aprofile'],
                        self.processAnalysisProfiles).start()

    def processSampleTypes(self):
        """
        Updates SampleTypes from Bika Instace.
        """
        try:
            imported = 0
            db_uids = self.db.get_uids('sampletypes')
            api_samtypes = self.api.getContent(
                            'SampleType',
                            inactive_state="active").get('items', {})
            if not api_samtypes or len(api_samtypes) == 0:
                print '[WARN] No Sample Types found in Bika'
            new_samtypes = [SampleType(uid=st['uid'],
                                       title=st['title'])
                            for st in api_samtypes
                            if st['uid'] not in db_uids]
            imported = len(new_samtypes)
            for st in new_samtypes:
                self.db.insert('sampletypes', st.get_db_format())
            message = str(imported) + ' Sample Types imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'SampleType')
        threading.Timer(intervals['sampletype'],
                        self.processSampleTypes).start()

    def processDiseases(self):
        """
        Updates Diseases from Bika Instace.
        """
        try:
            imported = 0
            db_uids = self.db.get_uids('diseases')
            api_diss = self.api.getContent('Disease').get('items', {})
            if not api_diss or len(api_diss) == 0:
                print '[WARN] No Diseases found in Bika'
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

    def processOutcomes(self):
        """
        Updates Case Outcomes from Bika Instance.
        """
        try:
            imported = 0
            db_uids = self.db.get_uids('caseoutcomes')
            api_cos = self.api.getContent('CaseOutcome').get('items', {})
            if not api_cos or len(api_cos) == 0:
                print '[WARN] No Case Outcomes found in Bika'
            new_cos = [CaseOutcome(uid=co['uid'],
                                   id=co['id'],
                                   title=co['title'])
                       for co in api_cos
                       if co['uid'] not in db_uids]
            imported = len(new_cos)
            for co in new_cos:
                self.db.insert('caseoutcomes', co.get_db_format())
            message = str(imported) + ' Case Outcomes imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'CaseOutcome')
        threading.Timer(intervals['caseoutcome'], self.processOutcomes).start()

    def processFacilities(self):
        """
        Updates Facilities (Clients in Bika) from Bika Instace.
        """
        try:
            imported = 0
            db_uids = self.db.get_uids('facilities')
            api_facs = self.api.getContent('Client', review_state='active'
                                           ).get('items', {})
            if not api_facs or len(api_facs) == 0:
                print '[WARN] No Health Facilities found in Bika'
            new_facs = [Facility(uid=f['uid'],
                                 code=f['id'],
                                 title=f['title'],
                                 county=f['getProvince'],
                                 district=f['getDistrict'])
                        for f in api_facs
                        if (f['uid'] not in db_uids \
                            and f['getCountry']=='Liberia')]
            imported = len(new_facs)
            for f in new_facs:
                self.db.insert('facilities', f.get_db_format())
            message = str(imported) + ' New Facilities imported.'
            status = 'Success'
        except Exception, e:
            message = str(e)
            status = 'Fail'
        self.insert_log(status, message, 'Facility')
        threading.Timer(intervals['facility'], self.processFacilities).start()

    def processForms(self):
        """
        This function gets all newly created IDSR forms and sends requests to
        API to create Patient and ARs.
        If API response of Patient creation is fail, it doesn't try to create
        an AR.
        If API response of AR creation is success, then it updates Form's
        'bika-status'.
        For each IDSR Form, 2 logs are inserted (one for Patient and one for
        AR).
        """
        print 'Submitting IDSR Forms to Bika...'
        try:
            forms = self.db.get_waiting_forms()
            for f in forms:
                # To create a new AR, Patient UID and Contact ID are required

                # PATIENT CREATION
                p_result = self.api.create(f.getPatient())
                if not p_result.get('success', ''):
                    message = p_result['message']
                    status = 'Fail'
                    self.db.update_status(f.getId(), 'failed')
                    self.insert_log(status, message,
                                    'Patient', f.getId())
                    continue
                p_id = p_result['obj_id']
                message = 'Patient Created. ID: '+p_id
                status = 'Success'
                self.insert_log(status, message,
                                'Patient', f.getId())
                p_uid = self.api.getUID(p_id, "Patient")

                # CLIENT CONTACT CREATION
                c_result = self.api.create(f.getContact())
                if not c_result.get('success', ''):
                    message = c_result['message']
                    status = 'Fail'
                    self.db.update_status(f.getId(), 'failed')
                    self.insert_log(status, message,
                                    'Contact', f.getId())
                    continue
                c_id = c_result['obj_id']
                message = 'Contact Created. ID: '+c_id
                status = 'Success'
                self.insert_log(status, message,
                                'Contact', f.getId())

                # FINALLY AR CREATION
                ar = f.getAR()
                ar.setPatientUid(p_uid)
                ar.setContactUid(c_id)
                ar_result = self.api.create(ar)
                if not ar_result.get('success', ''):
                    message = str(ar_result['message'])
                    status = 'Fail'
                    self.db.update_status(f.getId(), 'failed')
                    self.insert_log(status, message,
                                    'AnalysisRequest', f.getId())
                    continue
                message = 'AR Created. UID: '+ar_result.get('ar_id')
                status = 'Success'
                self.db.update_status(f.getId(), 'inserted')
                self.insert_log(status, message,
                                'AnalysisRequest', f.getId())
        except Exception, e:
            message = str(e)
            status = 'Fail'
            self.insert_log(status, message, 'AR & Patient')
        threading.Timer(intervals['idsrform'], self.processForms).start()

    def insert_log(self, status, message, content_type, idsr_id=None):
        """
        Inserts log of Sync Job to MongoDB.
        """
        print '{0}. {1}'.format(status, message)
        log = SyncJob(log_time=time.time(),
                      status=status,
                      message=message,
                      content_type=content_type
                      )
        if idsr_id:
            log.set_idsr_id(idsr_id)
        self.db.insert('syncjobs', log.get_db_format())


run = Run()
