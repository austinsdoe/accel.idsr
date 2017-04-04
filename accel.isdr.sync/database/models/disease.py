
class Disease():
    """
    Class that represents Disease
    """
    def __init__(self, uid, title):
        """
        Initializes the Disease object
        :param uid: UID of Disease from Plone
        :type uid: string
        :param title: the title of the Disease
        :type title: string
        """
        self.uid = uid
        self.title = title

    def get_title(self):
        return self.title

    def get_db_format(self):
        return {
            'uid': self.uid,
            'title': self.title
        }
