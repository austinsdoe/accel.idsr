
class Country():
    """
    Class that represents Country
    """
    def __init__(self, code, title):
        """
        Initializes the Country object
        :param code: the code of the Country
        :type code: string
        :param title: the title of the Country
        :type title: string
        """
        self.code = code
        self.title = title

    def get_title(self):
        return self.title

    def get_code(self):
        return self.code

    def get_db_format(self):
        return {
            'code': self.code,
            'title': self.title
        }
