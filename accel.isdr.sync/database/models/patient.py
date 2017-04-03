
class Patient():
    """
    Class that represents Patient
    """
    def __init__(self, clientPatientId, surname, firstname, birthDate,
                 gender, phone, healthCareFacility):
        self.clientPatientId = clientPatientId
        self.surname = surname
        self.firstname = firstname
        self.birthDate = birthDate
        self.gender = gender
        self.phone = phone
        self.healthCareFacility = healthCareFacility

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

    def getHealthCareFacility(self):
        return self.healthCareFacility
