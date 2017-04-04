
class AnalysisProfile():
    """
    Class that represents AnalysisProfile
    """
    def __init__(self, uid, title):
        """
        Initializes the AnalysisProfile object
        :param uid: UID of AnalysisProfile from Plone
        :type uid: string
        :param title: the title of the AnalysisProfile
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
