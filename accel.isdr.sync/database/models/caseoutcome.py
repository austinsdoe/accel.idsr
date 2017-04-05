
class CaseOutcome():
    """
    Class that represents CaseOutcome
    """
    def __init__(self, uid, id, title):
        """
        Initializes the CaseOutcome object
        :param uid: UID of CaseOutcome from Plone
        :type uid: string
        :param id: the id of the CaseOutcome generated in Bika Instance
        :type id: string
        :param title: the title of the CaseOutcome
        :type title: string
        """
        self.uid = uid
        self.id = id
        self.title = title

    def get_title(self):
        return self.title

    def get_db_format(self):
        return {
            'uid': self.uid,
            'id': self.id,
            'title': self.title
        }
