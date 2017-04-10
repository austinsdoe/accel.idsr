
class IDSRForm():
    """
    Class that represents IDSRForm
    From each IDSR Form record in DB, we can generate AR and Patient objects
    and assign them to one IDSRForm object in order not to lose AR-Patient
    relationship.
    """
    def __init__(self, form_id, patient, contact, ar):
        self.form_id = form_id
        self.patient = patient
        self.ar = ar
        self.contact = contact

    def getId(self):
        return self.form_id

    def getPatient(self):
        return self.patient

    def getAR(self):
        return self.ar

    def getContact(self):
        return self.contact
