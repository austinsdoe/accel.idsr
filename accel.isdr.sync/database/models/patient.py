from utils.config import settings


class Patient():
    """
    Class that represents Patient
    """

    def __init__(self, clientPatientId, is_anon, surname, firstname, birthDate,
                 gender, phone, facility_code):
        self.plone_site_name = settings['plone_site_name']
        self.clientPatientId = clientPatientId
        self.surname = surname
        self.firstname = firstname
        self.birthDate = birthDate
        self.gender = gender
        self.phone = phone
        self.facility_code = facility_code
        self.is_anon = is_anon

    def getClientPatientId(self):
        return self.clientPatientId

    def getSurname(self):
        return self.surname

    def getFirstname(self):
        return self.firstname

    def getBirthDate(self):
        return self.birthDate

    def getGender(self):
        return self.gender

    def getPhone(self):
        return self.phone

    def getFacilityCode(self):
        return self.facility_code

    def get_api_format(self):
        result = {
            "obj_path": '/' + self.plone_site_name+'/patients',
            "obj_type": 'Patient',
            "ClientPatientID": self.clientPatientId,
            "Surname": self.surname,
            "Firstname": self.firstname,
            "BirthDate": self.birthDate,
            "BirthDateEstimated": False,
            "Gender": self.gender,
            "HomePhone": self.phone,
            "MobilePhone": '',
            "BusinessPhone": '',
            "EmailAddress": '',
            "PatientAsGuarantor": True,
            "PrimaryReferrer": self.facility_code,
            "Anonymous": self.is_anon
        }
        if self.is_anon:
            result["Firstname"] = 'Anonymous'
            result["Surname"] = 'Patient'
        return result
