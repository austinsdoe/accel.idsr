
class Patient():
    """
    Class that represents Patient
    """
    def __init__(self, clientPatientId, surname, firstname, birthDate,
                 gender, phone, facility_code):
        self.clientPatientId = clientPatientId
        self.surname = surname
        self.firstname = firstname
        self.birthDate = birthDate
        self.gender = gender
        self.phone = phone
        self.facility_code = facility_code

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
            "obj_path": '/Plone/patients',
            "obj_type": 'Patient',
            "ClientPatientID": self.clientPatientId,
            "Surname": self.surname,
            "Firstname": self.firstname,
            "BirthDate": self.birthDate = birthDate,
            "BirthDateEstimated": False,
            "Gender": self.gender = gender,
            "HomePhone": self.phone,
            "MobilePhone": '',
            "BusinessPhone": '',
            "EmailAddress": '',
            "PatientAsGuarantor": False,
            "PrimaryReferrer": self.self.facility_code
        }
        return result
