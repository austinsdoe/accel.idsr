from accelidsr.mod_idsrentry import getDistrictChoices as _getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices as _getFacilityChoices

class IdsrJson:

    def getDistrictChoices(self, county=None):
        return _getDistrictChoices(county)

    def getFacilityChoices(self, county=None, district=None):
        return _getFacilityChoices(county, district)
