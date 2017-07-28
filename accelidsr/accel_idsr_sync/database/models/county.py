from ...utils.config import COUNTY_CODES
class County():
    """
    Class that represents County(Province/State)
    """
    def __init__(self, code, title):
        """
        Initializes the County object
        :param code: the code of the County
        :type code: string
        :param title: the title of the County
        :type title: string
        """
        self.code = code
        self.title = title

    def get_title(self):
        return self.title

    def get_code(self):
        for code in COUNTY_CODES:
            if self.code == code['bika_code']:
                self.code = code['tla']
        return self.code

    def get_db_format(self):
        return {
            'code': self.get_code(),
            'title': self.title
        }
