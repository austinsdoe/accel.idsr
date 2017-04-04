
class SampleType():
    """
    Class that represents SampleType
    """
    def __init__(self, uid, title):
        """
        Initializes the SampleType object
        :param uid: UID of SampleType from Plone
        :type uid: string
        :param title: the title of the SampleType
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
