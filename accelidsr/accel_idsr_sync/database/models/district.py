from ...utils.config import COUNTY_CODES


class District():
    """
    Class that represents District
    """
    def __init__(self, cocode, title):
        """
        Initializes the District object
        :param cocode: the county(province/state) code of the District
        :type cocode: string
        :param title: the title of the District
        :type title: string
        """
        self.cocode = cocode
        self.title = title

    def get_title(self):
        return self.title

    def get_cocode(self):
        for code in COUNTY_CODES:
            if self.cocode == code['bika_code']:
                self.cocode = code['tla']
        return self.cocode

    def get_db_format(self):
        return {
            'county_code': self.get_cocode(),
            'title': self.title
        }
