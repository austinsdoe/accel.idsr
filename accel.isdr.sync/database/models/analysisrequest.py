
class AnalysisRequest():
    """
    Class that represents AnalysisRequest.
    """
    def __init__(self, contact_uid, cc_contact, sampler_phone, case_id,
                 patient_record_id, reporting_health_facility, patient_uid,
                 sampling_date, sample_type, analysis_specification,
                 analyses_requested, client_order_number):
        # Contact UID
        self.contact_uid = contact_uid
        # CC Contact UID
        self.cc_contact = cc_contact
        # CCEmails in Bika
        self.sampler_phone = sampler_phone
        # Batch
        self.case_id = case_id
        self.patient_record_id = patient_record_id
        # Client in Bika
        self.reporting_health_facility = reporting_health_facility
        # Patient UID in Bika
        self.patient_uid = patient_uid
        self.sampling_date = sampling_date
        self.sample_type = sample_type
        # Specification UID
        self.analysis_specification = analysis_specification
        # Profiles in Bika
        self.analyses_requested = analyses_requested
        self.client_order_number = client_order_number

    def getContact(self):
        return self.contact

    def getCcContact(self):
        return self.cc_contact

    def getSamplerPhone(self):
        return self.sampler_phone

    def getCaseId(self):
        return self.case_id

    def getPatientRecordId(self):
        return self.patient_record_id

    def getPatientUid(self):
        return self.patient_uid

    def getSamplingDate(self):
        return self.sampling_date

    def getSampleType(self):
        return self.sample_type

    def getAnalysisSpecification(self):
        return self.analysis_specification

    def getAnalysesRequested(self):
        return self.analyses_requested

    def getClientOrderNumber(self):
        return self.client_order_number

    def setPatientUid(self, patient_uid):
        self.patient_uid = patient_uid

    def setPatientUid(self, contact_uid):
        self.contact_uid = contact_uid

    def get_api_format(self):
        result = {}
        result["0"] = {'Contact': self.contact_uid,
                       'CCContact': self.cc_contact,
                       'CCEmails': self.sampler_phone,
                       'Client': self.reporting_health_facility,
                       'Batch': self.case_id,
                       'ClientPatientID': self.patient_record_id,
                       'Patient': self.patient_uid,
                       'SamplingDate': self.sampling_date,
                       'SampleType': self.sample_type,
                       'Specification': '',
                       'ClientOrderNumber': self.client_order_number,
                       'Profiles': self.analyses_requested,
                       # TODO Analyses MUST BE REMOVED!
                       "Analyses": ["5d7c07665dfc43ddbb8d8c354740e412"]
                       }
        return result
