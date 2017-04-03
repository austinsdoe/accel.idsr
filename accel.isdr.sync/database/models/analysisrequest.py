
class AnalysisRequest():
    """
    Class that represents AnalysisRequest.
    """
    def __init__(self, contact, cc_contact, sampler_phone, case_id,
                 patient_record_id, patient, sampling_date, sample_type,
                 analysis_specification, client_order_number):
        self.contact = contact
        self.cc_contact = cc_contact
        self.sampler_phone = sampler_phone
        self.case_id = case_id
        self.patient_record_id = patient_record_id
        self.patient = patient
        self.sampling_date = sampling_date
        self.sample_type = sample_type
        self.analysis_specification = analysis_specification
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

    def getPatient(self):
        return self.patient

    def getSamplingDate(self):
        return self.sampling_date

    def getSampleType(self):
        return self.sample_type

    def getAnalysisSpecification(self):
        return self.analysis_specification

    def getClientOrderNumber(self):
        return self.client_order_number
