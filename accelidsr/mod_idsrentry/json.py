from accelidsr.mod_idsrentry import getDistrictChoices as _getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices as _getFacilityChoices


class IdsrJson:
    """
    Class that provides the functions that can be accessed through ajax calls
    via accelidsr.mod_idsrentry.controllers.json(func) function
    """
    def getDistrictChoices(self, county=None):
        """
        Returns a list of 2-tuples that contains the districts available in the
        system for the county passed in, sorted by the district name asc. Each
        element within the list is a 2-tuple, where the first element is the
        value to be used in the html control and the second item is the text to
        be displayed:
            [('val1', 'text1'), (val2, text2)]
        An additional tuple is added in the first position:
            [(''), 'Select...']
        If no county is passed in, a list with only the first record
        'Select...' is returned.

        :param county: A single string that identifies a county
        :type county: string
        :return: A list of 2-tuples with the districts sorted by name
            ascending, with an additional item in position 0: ('', 'Select...')
        :rtype: A list of 2-tuples
        """
        return _getDistrictChoices(county)

    def getFacilityChoices(self, county=None, district=None):
        """
        Returns a list of 2-tuples that contains the health facilities
        available in the system for the county and district passed in, sorted
        by the district name ascending. Each element within the list is a
        2-tuple, where the first element is the value to be used in the html
        control and the second item is the text to be displayed:
            [('val1', 'text1'), (val2, text2)]
        An additional tuple is added in the first position:
            [(''), 'Select...']
        If no county and/or no district is passed in, a list with only the
        first record 'Select...' is returned.

        :param county: A single string that identifies a county
        :type county: string
        :param district: A single string that identifies a district
        :type district: A string
        :return: A list of 2-tuples with the facilities sorted by name
            ascending, with an additional item in position 0: ('', 'Select...')
        :rtype: A list of 2-tuples
        """
        return _getFacilityChoices(county, district)
