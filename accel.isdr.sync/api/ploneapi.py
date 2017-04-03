from utils import config
from utils.config import settings
import json
import urllib
import urllib2


class PloneApi:
    def __init__(self):
        self.plone_site_url = settings['plone_site_url']
        self.jsonapi_url = '/'.join([self.plone_site_url, '@@API'])
        self.username = settings['jsonapi_username']
        self.password = settings['jsonapi_password']
        # We will attempt to connect at first startup, and so there is a
        # requirement that a Bika LIMS server can be contacted before this
        # application will start!
        self.opener = self._connect()

    def _connect(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        login_url = '/'.join([self.plone_site_url, 'login_form'])
        try:
            params = urllib.urlencode({
                "form.submitted": 1,
                "pwd_empty": 0,
                "__ac_name": self.username,
                "__ac_password": self.password,
                "submit": "Log in"
            })
            f = opener.open(login_url, params)
            data = f.read()
            f.close()
            return opener
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise RuntimeError(
                    "Login page at '%s' was not found (404)." % login_url)
        except urllib2.URLError as e:
            if e.reason.errno == 111:
                raise RuntimeError(
                    "Bika LIMS server at '%s' cannot be contacted (111)." %
                    self.plone_site_url)

    def getContents(self, content_type):
        url = self.jsonapi_url + '/plone/api/1.0/search?portal_type='\
            + content_type
        f = self.opener.open(url)
        data = f.read()
        f.close()
        return json.loads(data)

    def getCountries(self):
        url = self.plone_site_url + '/getCountries'
        # Setting some obligatory parameters
        params = urllib.urlencode({
            "searchTerm": '',
            "page": 1,
            "rows": 1000,
            "sord": '',
            "sidx": ''
        })
        f = self.opener.open(url, params)
        data = f.read()
        f.close()
        return json.loads(data)

    def getDistricts(self):
        url = self.plone_site_url + '/getGeoDistricts'
        # Getting all districts without setting any country or state
        params = urllib.urlencode({
            "getAll": 1,
        })
        f = self.opener.open(url, params)
        data = f.read()
        f.close()
        return json.loads(data)

    def createPatient(self, patient):
        url = self.jsonapi_url + '/create'
        # Setting some obligatory parameters
        params = urllib.urlencode({
            "obj_path": '/Plone/patients',
            "obj_type": 'Patient',
            "ClientPatientID": patient.getClientPatientId(),
            "Surname": patient.getSurname(),
            "Firstname": patient.getFirstname(),
            "BirthDate": patient.getBirthDate(),
            "BirthDateEstimated": False,
            "Gender": patient.getGender(),
            "HomePhone": patient.getPhone(),
            "MobilePhone": '',
            "BusinessPhone": '',
            "EmailAddress": '',
            "PatientAsGuarantor": False,
            "PrimaryReferrer": patient.getHealthCareFacility()
        })
        f = self.opener.open(url, params)
        data = f.read()
        f.close()
        return json.loads(data)

    def createContact(self, contact):
        url = self.jsonapi_url + '/create'
        # Setting some obligatory parameters
        params = urllib.urlencode({
            "obj_path": '/Plone/clients/'+contact.getClientId(),
            "obj_type": 'Contact',
            "Surname": contact.getSurname(),
            "Firstname": contact.getFirstname()
        })
        f = self.opener.open(url, params)
        data = f.read()
        f.close()
        return json.loads(data)

    def createAR(self, ar):
        url = self.plone_site_url + '/analysisrequest_submit'
        # Setting some obligatory parameters
        params = urllib.urlencode({
            "state": json.dumps(ar.get_api_format())
        })
        try:
            f = self.opener.open(url, params)
            data = f.read()
            f.close()
            return json.loads(data)
        except Exception, e:
            return {"errors": str(e)}

    def getPatientUID(self, obj_id):
        url = self.jsonapi_url + '/plone/api/1.0/search?id='+obj_id
        f = self.opener.open(url)
        data = f.read()
        f.close()
        result = json.loads(data)
        return result['items'][0]['uid']

    def getContactUID(self, client_id, obj_id):
        url = self.jsonapi_url + '/plone/api/1.0/search?id='+obj_id + \
            '&folder='+client_id
        f = self.opener.open(url)
        data = f.read()
        f.close()
        result = json.loads(data)
        return result['items'][0]['uid']
