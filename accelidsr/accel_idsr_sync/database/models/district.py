
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
        return self.cocode

    def get_db_format(self):
        return {
            'county_code': self.cocode,
            'title': self.title
        }
