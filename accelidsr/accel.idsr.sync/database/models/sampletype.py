
class SampleType():
    """
    Class that represents SampleType
    """
    def __init__(self, uid, id, title):
        """
        Initializes the SampleType object
        :param uid: UID of SampleType from Plone
        :type uid: string
        :param id: ID of SampleType from Plone
        :type id: string
        :param title: the title of the SampleType
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
