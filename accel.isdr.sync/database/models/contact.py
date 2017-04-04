
class Contact():
    """
    Class that represents Contact.
    """
    def __init__(self, client_id, firstname, surname):
        self.firstname = firstname
        self.surname = surname
        self.client_id = client_id

    def getFirstname(self):
        return self.firstname

    def getSurname(self):
        return self.surname

    def getClientId(self):
        return self.client_id

    def get_api_format(self):
        result = {
            "obj_path": '/Plone/clients/'+self.client_id,
            "obj_type": 'Contact',
            "Surname": self.surname,
            "Firstname": self.firstname
        }
        return result
