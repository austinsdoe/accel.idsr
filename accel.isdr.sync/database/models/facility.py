
class Facility():
    """
    Class that represents Health Care Facility (Client in Bika)
    """
    def __init__(self, uid, code, title, county, district):
        """
        Initializes the Facility object
        :param uid: UID of Facility(Client) from Plone
        :type uid: string
        :param code: the code of the Facility (id of Client in Bika)
        :type code: string
        :param title: the title of the Facility(Client)
        :type title: string
        :param county: the county name of the Facility(Client)
        :type county: string
        :param district: the title of the Facility(Client)
        :type title: string
        """
        self.uid = uid
        self.code = code
        self.title = title
        self.county = county
        self.district = district

    def get_title(self):
        return self.title

    def get_db_format(self):
        return {
            'uid': self.uid,
            'code': self.code,
            'title': self.title,
            'county': self.county,
            'district': self.district
        }
